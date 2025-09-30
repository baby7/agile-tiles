import ctypes
import os
import re
import sys
import time
import subprocess

# 打包命令
"""
nuitka \
--mingw64 \
--onefile \
--standalone \
--windows-console-mode=disable \
--windows-icon-from-ico=resources/img/icon/icon.ico \
--output-dir=out \
--windows-company-name=杭州市拱墅区启杭灵卡软件开发工作室 \
--windows-product-name=灵卡面板 \
--windows-file-version=1.0.0 \
--windows-product-version=1.0.0 \
--windows-file-description=灵卡面板全量更新工具 \
--lto=yes \
--jobs=8 \
--show-progress \
--show-memory \
full_updater.py
"""

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
                subprocess.run(['taskkill', '/pid', task_pid, '/f'], check=True, shell=True,
                               creationflags=subprocess.CREATE_NO_WINDOW)
                print(f"已终止进程: {task_pid}")
                return True
    except subprocess.CalledProcessError as e:
        print(f"执行命令失败: {e}")
    except Exception as e:
        print(f"错误: {e}")

    return False

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def kill_exe(current_exe):
    # 尝试杀死可能还在运行的进程
    print("尝试终止可能还在运行的进程...")
    killed = kill_process_by_exe_path(current_exe)
    if killed:
        print("成功终止了进程")
        time.sleep(0.5)  # 给系统一点时间释放资源
    else:
        print("没有找到需要终止的进程")

def parse_filename(filename):
    pattern = r'^AgileTilesSetupV(\d+)\.(\d+)\.(\d+)\.exe$'
    match = re.match(pattern, filename)

    if match:
        major, minor, patch = map(int, match.groups())
        return True, (major, minor, patch)
    else:
        return False, None

def main():
    # 检查管理员权限，如果需要则提升
    if not is_admin():
        import ctypes
        # 尝试以管理员权限重新运行
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

    # 创建应用程序实例，不显示控制台窗口
    if sys.platform == "win32":
        import ctypes
        # 隐藏控制台窗口（如果是从命令行启动的）
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

    current_exe = os.path.join(os.getcwd(), "AgileTiles.exe")               # 当前主程序的exe路径
    kill_exe(current_exe)

    app_name = "AgileTiles"

    data_parent_dir = os.environ['LOCALAPPDATA']
    data_dir = os.path.join(data_parent_dir, app_name)
    update_dir = os.path.join(data_dir, "UpdateCache")

    # 获取最新安装包
    setup_exe_path = None
    setup_exe_version = 0
    for file_name in os.listdir(update_dir):
        # 判断文件还是文件夹
        if not os.path.isfile(os.path.join(update_dir, file_name)):
            continue
        # 判断文件名前缀格式
        is_valid, version = parse_filename(file_name)
        if not is_valid:
            continue
        (major, minor, patch) = version
        current_file_version = major * 1000000 + minor * 1000 + patch
        if current_file_version > setup_exe_version:
            setup_exe_path = os.path.join(update_dir, file_name)
            setup_exe_version = current_file_version

    # 尝试其他名称的安装包
    if setup_exe_path is None:
        if os.path.exists(os.path.join(update_dir, "AgileTilesSetup.exe")):
            setup_exe_path = os.path.join(update_dir, "AgileTilesSetup.exe")
        elif os.path.exists(os.path.join(update_dir, "AgileTilesSetup.msi")):
            setup_exe_path = os.path.join(update_dir, "AgileTilesSetup.msi")
        elif os.path.exists(os.path.join(update_dir, "setup.exe")):
            setup_exe_path = os.path.join(update_dir, "setup.exe")
        elif os.path.exists(os.path.join(update_dir, "setup.msi")):
            setup_exe_path = os.path.join(update_dir, "setup.msi")
    if setup_exe_path is None:
        print("未找到安装包")
        return

    # 启动安装包
    try:
        subprocess.Popen(setup_exe_path, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        print(f"启动安装包失败: {str(e)}")
        sys.exit(1)
    print("正在启动安装包...")
    sys.exit(0)

if __name__ == "__main__":
    main()
