import os
import shutil
import subprocess
from src.constant.current_version_info import current_version


# 定义版本号
version = current_version.replace("v", "V")
no_v_version = current_version.replace("v", "").replace("V", "")
# 目标目录
output_dir = f"dist/AgileTiles{version}"


# 步骤3: 执行 Pyinstaller 编译命令
print("开始执行 Pyinstaller 编译命令")
pyinstaller_command = [
    "pyinstaller",

    "--clean",                                                                      # (--clean)清理构建目录
    "-F",                                                                           # (--onefile)打包为单个文件
    # "-w",                                                                           # (--windowed)隐藏控制台窗口
    "--icon=resources/img/icon/icon.ico",                                           # (--icon)图标路径
    f"--distpath={output_dir}",                                                     # (--distpath)输出路径
    "--name=AgileTiles",                                                            # (--name)输出文件名

    "AgileTiles.py"
]

process = subprocess.run(pyinstaller_command, check=True, shell=True)
print("完成 Pyinstaller 编译命令")


# 步骤4: 复制 ./static 文件夹的内容到目标目录
def copy_files(src, dst):
    print(f"正在复制文件夹 {src} 到 {dst}")
    # 检查源文件夹是否为空
    if not any(os.listdir(src)):
        print(f"警告：源文件夹 {src} 为空，跳过复制。")
        return
    if os.path.exists(dst):
        shutil.rmtree(dst)
    # 忽略 .py 和 .pyc 文件
    ignore_patterns = shutil.ignore_patterns('*.py', '*.pyc')
    shutil.copytree(src, dst, ignore=ignore_patterns)
    print(f"完成复制文件夹 {src} 到 {dst}")

# 步骤6: 复制 static 文件夹
copy_files("static", f"{output_dir}/static")
print("完成复制 static 文件夹")

# 步骤6.1: 删除特定的文件(如果存在)
if os.path.exists(f"{output_dir}/static/thirdparty/everything/Everything.db"):
    os.remove(f"{output_dir}/static/thirdparty/everything/Everything.db")
if os.path.exists(f"{output_dir}/static/thirdparty/everything/Everything.db.tmp"):
    os.remove(f"{output_dir}/static/thirdparty/everything/Everything.db.tmp")
if os.path.exists(f"{output_dir}/static/thirdparty/everything/Everything.ini"):
    os.remove(f"{output_dir}/static/thirdparty/everything/Everything.ini")

# 步骤7: 复制 licenses 文件夹
copy_files("licenses", f"{output_dir}/licenses")
print("完成复制 licenses 文件夹")

# 步骤8: 复制 doc 文件夹
copy_files("doc", f"{output_dir}/doc")
print("完成复制 doc 文件夹")

# 步骤9: 复制 run_util 文件夹
shutil.copyfile("run_util/login_helper.exe", f"{output_dir}/login_helper.exe")
shutil.copyfile("run_util/patch_updater.exe", f"{output_dir}/patch_updater.exe")
shutil.copyfile("run_util/full_updater.exe", f"{output_dir}/full_updater.exe")
print("完成复制 run_util 文件夹")

print("所有步骤已完成！")