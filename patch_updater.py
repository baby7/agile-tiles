import os
import shutil
import sys
import time
import subprocess


# 打包命令
# nuitka --onefile --standalone --windows-console-mode=disable --windows-icon-from-ico=run_util/util.ico --output-dir=out --windows-uac-admin --lto=yes --jobs=8 --show-progress --show-memory patch_updater.py

def kill_process_by_exe_path(exe_path):
    """根据exe路径杀死进程（纯Windows命令实现）"""
    exe_path = os.path.abspath(exe_path)
    exe_name = os.path.basename(exe_path)
    print(f"程序名称:{exe_name}")
    try:
        # 使用tasklist命令查找进程
        result = subprocess.run(
            ['tasklist', '/fo', 'csv', '/nh'],
            capture_output=True, text=True, check=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        # 解析输出，查找匹配的进程
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if not line:
                continue
            parts = line.split('","')
            task_name = parts[0].strip('"')
            task_pid = parts[1].strip('"')
            if len(parts) >= 5 and exe_name == task_name:
                print("找到进程: PID={}, 名称={}".format(task_pid, task_name))
                # 终止进程
                subprocess.run(['taskkill', '/pid', task_pid, '/f'], check=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                print(f"已终止进程: {task_pid}")
                return True
    except subprocess.CalledProcessError as e:
        print(f"执行命令失败: {e}")
    except Exception as e:
        print(f"错误: {e}")

    return False


def main():
    current_exe = os.path.join(os.getcwd(), "AgileTiles.exe")               # 当前主程序的exe路径
    new_exe = os.path.join(os.getcwd(), "temp_updates", "AgileTiles.exe")   # 新下载的exe路径
    restart_command = current_exe                                           # 重启主程序的命令

    print(f"当前程序: {current_exe}")
    print(f"新程序: {new_exe}")
    print(f"重启命令: {restart_command}")

    # 等待主程序退出
    time.sleep(2)

    print(f"current_exe:{current_exe}")
    # 尝试杀死可能还在运行的进程
    print("尝试终止可能还在运行的进程...")
    killed = kill_process_by_exe_path(current_exe)
    if killed:
        print("成功终止了进程")
        time.sleep(1)  # 给系统一点时间释放资源
    else:
        print("没有找到需要终止的进程")

    # 尝试替换文件
    max_attempts = 3  # 增加重试次数
    for attempt in range(max_attempts):
        try:
            # 备份当前exe（如果存在）
            backup_exe = current_exe + ".bak"
            if os.path.exists(backup_exe):
                try:
                    os.remove(backup_exe)
                except:
                    pass  # 忽略删除备份文件的错误

            # 重命名当前exe为备份
            if os.path.exists(current_exe):
                os.rename(current_exe, backup_exe)

            # 复制新exe
            shutil.copy2(new_exe, current_exe)

            # 删除备份文件
            if os.path.exists(backup_exe):
                try:
                    os.remove(backup_exe)
                except:
                    pass  # 忽略删除备份文件的错误

            print("更新成功")
            break
        except Exception as e:
            print(f"尝试 {attempt + 1} 失败: {str(e)}")

            # 如果是因为文件被占用，尝试再次杀死进程
            if "being used by another process" in str(e) or "另一个程序正在使用" in str(e):
                print("文件被占用，尝试再次终止进程...")
                kill_process_by_exe_path(current_exe)
                time.sleep(2)

            time.sleep(1)  # 等待一段时间后重试
    else:
        print("更新失败，无法替换文件")
        sys.exit(1)

    # 启动新的主程序
    try:
        subprocess.Popen(restart_command, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        print(f"启动主程序失败: {str(e)}")
        sys.exit(1)

    print("更新完成，正在启动新程序...")
    sys.exit(0)


if __name__ == "__main__":
    main()