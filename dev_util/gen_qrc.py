# 注意，此程序只针对windows，windows下文件（夹）名不区分大小写
import os.path


qrc_str = """<!DOCTYPE RCC>
<RCC>
    <qresource>
"""

# 读入指定目录并转换为绝对路径
rootdir = os.path.abspath("D:/project/python/agile-tiles/resources/img")
# 先修改文件名
for parent, dirnames, filenames in os.walk(rootdir):
    for filename in filenames:
        pathfile = os.path.join(parent, filename)
        pathfile = pathfile.replace("\\", "/")
        qrc_path = "resources/img" + pathfile.split("resources/img")[1]
        alias_path = "static/img" + pathfile.split("resources/img")[1]
        qrc_str += f"        <file alias=\"{alias_path}\">{qrc_path}</file>\n"

qrc_str += """    </qresource>
</RCC>"""

print(qrc_str)

# 写入qrc文件
with open("/resources_qrc/compiled_resources.qrc", "w", encoding="utf-8") as f:
    f.write(qrc_str)