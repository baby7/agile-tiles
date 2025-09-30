import os
import shutil
import zipfile


def get_file_size(file_path):
    """
    获取文件大小，返回一个带有单位的字符串表示。
    :param file_path: 文件路径
    :return: 带有单位的文件大小字符串
    """
    # 获取文件大小，单位为字节
    size = os.path.getsize(file_path)
    # 定义单位和对应的换算系数
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    factor = 1024
    # 计算合适的单位
    for unit in units:
        if size < factor:
            return f"{size:.2f} {unit}"
        size /= factor
    return f"{size:.2f} {units[-1]}"


def get_txt_file_words_number(file_path, encodings):
    """
    获取txt文件中的字数。
    :param file_path: 文件路径
    :return: 带有单位的字数字符串
    """
    try:
        with open(file_path, 'r', encoding=encodings) as file:
            content = file.read()
            char_count = len(content)
            return f"{char_count}字"
    except FileNotFoundError:
        return "文件未找到"
    except Exception as e:
        return f"发生错误: {str(e)}"


def extract_zip(zip_path, target_folder):
    try:
        # 创建目标文件夹（如果不存在）
        os.makedirs(target_folder, exist_ok=True)
        # 解压ZIP文件
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(target_folder)
        print(f"成功将 {zip_path} 解压到 {target_folder}")
        return True
    except FileNotFoundError:
        print(f"错误：ZIP文件 {zip_path} 不存在")
    except zipfile.BadZipFile:
        print(f"错误：{zip_path} 不是有效的ZIP文件")
    except Exception as e:
        print(f"解压过程中发生未知错误: {str(e)}")
    return False


def atomic_delete(path: str) -> bool:
    """原子性删除目录（全删或保留）"""
    temp_name = None
    try:
        # 尝试重命名以检测文件占用
        temp_name = os.path.join(os.path.dirname(path), f"_{os.path.basename(path)}")
        os.rename(path, temp_name)
        print(f"重命名成功：{path} -> {temp_name}")
        # 执行实际删除
        shutil.rmtree(temp_name)
        return True
    except Exception as e:
        print(f"删除失败 {path}，原因：{str(e)}")
        # 恢复重命名（如果部分成功）
        if temp_name and os.path.exists(temp_name):
            try:
                print(f"恢复重命名：{temp_name} -> {path}")
                os.rename(temp_name, path)
            except Exception as rollback_e:
                print(f"回滚失败：{rollback_e}")
        return False

def get_app_data_path(app_name):
    # 获取应用程序数据目录（跨平台）
    # Windows: C:\Users\<User>\AppData\Local\<AppName>
    # macOS: ~/Library/Application Support/<AppName>
    # Linux: ~/.local/share/<AppName>
    data_parent_dir = os.environ['LOCALAPPDATA']
    data_dir = os.path.join(data_parent_dir, app_name)
    print(f"获取软件数据目录:{data_dir}")
    if not data_dir:  # 确保目录有效
        data_dir = os.path.expanduser("~")  # 回退到用户目录
    # 创建目录
    try:
        os.makedirs(data_dir, exist_ok=True)
    except OSError as e:
        print(f"无法创建目录 {data_dir}: {e}")
        return None  # 或抛出异常
    return data_dir

def get_app_data_db_path(app_data_path, app_name):
    # 跨平台安全拼接路径
    old_db_dir = os.path.join(app_data_path, app_name)
    old_db_file = os.path.join(str(old_db_dir), "app.db")
    db_dir = os.path.join(app_data_path, "DB")
    db_file = os.path.join(str(db_dir), "app.db")
    # 如果新目录不存在，则创建
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    # 如果旧数据库存在且新数据库不存在，则移动旧数据库到新目录
    if os.path.exists(old_db_file) and not os.path.exists(db_file):
        # 移动旧数据库到新目录
        shutil.move(str(old_db_file), str(db_dir))
    # 删除旧数据库
    if os.path.exists(old_db_file):
        os.remove(old_db_file)
    # 删除旧目录
    if os.path.exists(old_db_dir):
        shutil.rmtree(old_db_dir)
    return db_file

def get_app_data_plugin_path(app_data_path):
    # 跨平台安全拼接路径
    plugin_dir = os.path.join(app_data_path, "Plugin")
    print(f"程序插件目录:{plugin_dir}")
    try:
        os.makedirs(plugin_dir, exist_ok=True)
    except OSError as e:
        print(f"无法创建目录 {plugin_dir}: {e}")
        return None  # 或抛出异常
    return plugin_dir

def get_app_data_network_path(app_data_path):
    # 跨平台安全拼接路径
    network_dir = os.path.join(app_data_path, "NetworkCache")
    print(f"程序网络缓存目录:{network_dir}")
    try:
        os.makedirs(network_dir, exist_ok=True)
    except OSError as e:
        print(f"无法创建目录 {network_dir}: {e}")
        return None  # 或抛出异常
    return network_dir

def get_app_data_image_path(app_data_path):
    # 跨平台安全拼接路径
    image_dir = os.path.join(app_data_path, "ImageCache")
    print(f"程序图片缓存目录:{image_dir}")
    try:
        os.makedirs(image_dir, exist_ok=True)
    except OSError as e:
        print(f"无法创建目录 {image_dir}: {e}")
        return None  # 或抛出异常
    return image_dir

def get_app_data_update_path(app_data_path):
    # 跨平台安全拼接路径
    update_dir = os.path.join(app_data_path, "UpdateCache")
    print(f"程序更新缓存目录:{update_dir}")
    try:
        os.makedirs(update_dir, exist_ok=True)
    except OSError as e:
        print(f"无法创建目录 {update_dir}: {e}")
        return None  # 或抛出异常
    return update_dir
