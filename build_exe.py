import os
import shutil
import subprocess
from src.constant.current_version_info import current_version


# 定义版本号
version = current_version.replace("v", "V")
no_v_version = current_version.replace("v", "").replace("V", "")
# 目标目录
output_dir = f"out/AgileTiles{version}"


# 步骤1: 删除"out/AgileTiles.dist"文件夹
if os.path.exists("out/AgileTiles.dist"):
    shutil.rmtree("out/AgileTiles.dist")
    print("完成删除 out/AgileTiles.dist 文件夹")

# 步骤2: 删除"out/AgileTiles.build"文件夹
if os.path.exists("out/AgileTiles.build"):
    shutil.rmtree("out/AgileTiles.build")
    print("完成删除 out/AgileTiles.build 文件夹")

# 步骤3: 执行 Nuitka 2.7.12 编译命令
print("开始执行 Nuitka 编译命令")
nuitka_command = [
    "nuitka",

    "--mingw64",                                                            # 使用 MinGW64 编译器
    "--standalone",                                                         # 生成一个包含所有依赖的文件夹，里面有可执行文件和依赖。
    # "--windows-console-mode=disable",                                       # 禁用控制台窗口

    "--enable-plugin=pyside6",                                              # 使用 PySide6 插件
    "--disable-plugin=pyqt5,pyqt6",                                         # 禁用 PyQt5 和 PyQt6 插件
    "--include-qt-plugins=multimedia",                                      # 音乐播放器需要用到multimedia
    "--include-package=wmi",                                                # wmi包
    "--include-package=win32com",                                           # pywin32的核心包
    "--include-package=pywintypes",                                         # pywin32的核心包

    "--windows-icon-from-ico=resources/img/icon/icon.ico",                     # 图标路径
    "--output-dir=out",                                                     # 输出目录

    "--windows-company-name=杭州市拱墅区启杭灵卡软件开发工作室",                  # Windows下软件公司信息
    "--windows-product-name=灵卡面板",                                       # Windows下软件名称
    "--windows-file-version=" + no_v_version,                               # Windows下软件的版本
    "--windows-product-version=" + no_v_version,                            # Windows下软件的产品版本
    "--windows-file-description=灵卡面板",                                  # Windows下软件的作用描述

    # "--windows-uac-admin",                                                  # 管理员权限的清单文件

    "--lto=yes",                                                            # 启用 Link Time Optimization（LTO）以优化编译速度和性能。
    "--jobs=14",                                                            # 使用 16 个线程并行编译，加速编译速度。
    "--show-progress",                                                      # 显示编译进度。
    "--show-memory",                                                        # 显示内存使用情况。

    "AgileTiles.py"
]

process = subprocess.run(nuitka_command, check=True, shell=True)
print("完成 Nuitka 编译命令")


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


# 步骤5: 重命名文件夹AgileTiles.dist为AgileTiles
shutil.move("out/AgileTiles.dist", output_dir)
print("正在重命名文件夹 AgileTiles.dist 为 AgileTiles")

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
shutil.copyfile("run_util/exit_helper.exe", f"{output_dir}/exit_helper.exe")
print("完成复制 run_util 文件夹")

# 步骤10: 删除"out/AgileTiles.dist"文件夹
if os.path.exists("out/AgileTiles.dist"):
    shutil.rmtree("out/AgileTiles.dist")
    print("完成删除 out/AgileTiles.dist 文件夹")

# 步骤11: 删除"out/AgileTiles.build"文件夹
if os.path.exists("out/AgileTiles.build"):
    shutil.rmtree("out/AgileTiles.build")
    print("完成删除 out/AgileTiles.build 文件夹")

print("所有步骤已完成！")