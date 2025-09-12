import os
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
--windows-icon-from-ico=run_util/util.ico \
--output-dir=out \
--windows-company-name=杭州市拱墅区启杭灵卡软件开发工作室 \
--windows-product-name=灵卡面板 \
--windows-file-version=1.0.0 \
--windows-product-version=1.0.0 \
--windows-file-description=灵卡面板退出工具 \
--windows-uac-admin \
--lto=yes \
--jobs=8 \
--show-progress \
--show-memory \
exit_helper.py
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
    print(f"当前程序: {current_exe}")

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
    sys.exit(0)


if __name__ == "__main__":
    main()
