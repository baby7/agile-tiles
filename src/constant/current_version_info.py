from src.constant import version_constant

current_version = list(version_constant.update_map_info.keys())[-1]
print("当前版本: " + current_version)