import json
import sqlite3

from src.module.UserData.DataBase import user_data_common

from src.util import hardware_id_util


class DatabaseManager:
    def __init__(self, db_path=None):
        self.db_path = db_path
        self.FIXED_SALT = b'c093dd8c-c3da-4201-b291-ec4482fd624b'  # 32字节固定盐值
        self._init_db()

    def _init_db(self):
        """初始化数据库表结构"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # 创建用户表（移除salt列）
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    refresh_token TEXT NOT NULL,
                    last_login DATETIME
                )
            """)
            # 创建用户数据表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    data TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    modified_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    source TEXT CHECK(source IN ('local', 'cloud')) DEFAULT 'local',
                    is_current BOOLEAN DEFAULT 1,
                    sync_status TEXT CHECK(sync_status IN ('pending', 'synced', 'conflict')) DEFAULT 'pending',
                    backup_tag TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            # 创建索引
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON user_data(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_sync_status ON user_data(sync_status)")
            conn.commit()

    def get_current_user(self):
        """获取最近登录的用户"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username, refresh_token FROM users WHERE last_login IS NOT NULL ORDER BY last_login DESC LIMIT 1"
            )
            result = cursor.fetchone()
            if not result:
                print("没有最近登录的用户")
                return None
            return {
                "username": result[0],
                "refreshToken": result[1]
            }

    def logout_user(self):
        """注销当前用户（清除最后登录时间）"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET last_login = NULL WHERE last_login IS NOT NULL"
            )
            conn.commit()

    def register_user(self, username, refresh_token):
        """注册新用户"""
        print(f"开始注册用户:{username},{refresh_token}")
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, refresh_token) VALUES (?, ?)",
                    (username, refresh_token))
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # 用户名已存在

    def update_user_refresh_token(self, username, refresh_token):
        """更新用户刷新令牌"""
        print(f"更新用户刷新令牌:{username},{refresh_token}")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET refresh_token = ? WHERE username = ?",
                (refresh_token, username)
            )
            conn.commit()

    def update_last_login(self, username):
        """更新用户最后登录时间"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET last_login = datetime('now') WHERE username = ?",
                (username,)
            )
            conn.commit()

    def save_user_data(self, username, data, source='local', backup_tag=None):
        """保存用户数据并标记为当前版本"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # 获取用户ID
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            user_id = cursor.fetchone()[0]

            # 将旧数据标记为非当前
            cursor.execute(
                "UPDATE user_data SET is_current = 0 WHERE user_id = ?",
                (user_id,)
            )

            # 插入新数据
            cursor.execute(
                """INSERT INTO user_data 
                (user_id, data, source, backup_tag, modified_at, sync_status) 
                VALUES (?, ?, ?, ?, datetime('now'), 'pending')""",
                (user_id, data, source, backup_tag)
            )
            conn.commit()

    def get_current_data(self, username):
        """获取用户的当前数据"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT data FROM user_data 
                WHERE user_id = (SELECT id FROM users WHERE username = ?) 
                AND is_current = 1
            """, (username,))
            result = cursor.fetchone()
            return result[0] if result else None

    def get_user_backups(self, username):
        """获取用户的所有备份数据"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, data, created_at, modified_at, source, backup_tag, sync_status 
                FROM user_data 
                WHERE user_id = (SELECT id FROM users WHERE username = ?)
                ORDER BY modified_at DESC
            """, (username,))
            return cursor.fetchall()

    def get_unsynced_data(self, username):
        """获取待同步的数据"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, data, modified_at 
                FROM user_data 
                WHERE user_id = (SELECT id FROM users WHERE username = ?)
                AND sync_status = 'pending'
                ORDER BY modified_at DESC
            """, (username,))
            return cursor.fetchall()

    def mark_as_synced(self, record_id):
        """标记数据为已同步"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE user_data SET sync_status = 'synced' WHERE id = ?",
                (record_id,)
            )
            conn.commit()

    def restore_backup(self, backup_id):
        """恢复指定备份为当前版本"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # 获取备份所属用户
            cursor.execute("SELECT user_id FROM user_data WHERE id = ?", (backup_id,))
            user_id = cursor.fetchone()[0]

            # 将所有数据标记为非当前
            cursor.execute(
                "UPDATE user_data SET is_current = 0 WHERE user_id = ?",
                (user_id,)
            )

            # 将指定备份标记为当前
            cursor.execute(
                "UPDATE user_data SET is_current = 1 WHERE id = ?",
                (backup_id,)
            )
            conn.commit()

    def save_default_data(self, username, hardware_id):
        if hardware_id is None:
            hardware_id = hardware_id_util.get_hardware_id()
        data = user_data_common.get_data(hardware_id)
        self.save_user_data(username, json.dumps(data).encode('utf-8'), source='local', backup_tag='default')
        return data