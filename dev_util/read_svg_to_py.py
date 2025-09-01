# 注意，此程序只针对windows，windows下文件（夹）名不区分大小写
import os.path


svg_map = {}

# 读入指定目录并转换为绝对路径
rootdir = os.path.abspath("/resources/img/IconPark/svg")
# 先修改文件名
for parent, dirnames, filenames in os.walk(rootdir):
    for filename in filenames:
        pathfile = os.path.join(parent, filename)
        if pathfile is not None and pathfile != "":
            # 读取svg字符串
            svg_str = open(pathfile, "r", encoding="utf-8").read()
            # 处理掉蓝色底色
            svg_str = (svg_str
                       .replace(' fill="#2F88FF"', "")
                       .replace(' fill="#43CCF8"', "")
                       .replace('white', "black"))
            # 分组
            svg_end_path = pathfile.split("IconPark")[1].replace("\\svg\\", "").replace(".svg", "")
            svg_type = svg_end_path.split("\\")[0]
            svg_name = svg_end_path.split("\\")[1]
            if svg_type not in svg_map:
                svg_map[svg_type] = {}
            svg_map[svg_type][svg_name] = svg_str

# 将svg映射写入txt文件
with open("/src/ui/svg_dict.py", "w", encoding="utf-8") as f:
    f.write("svg_dict=" + str(svg_map))