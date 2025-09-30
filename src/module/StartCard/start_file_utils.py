import os
import json

def scan_local_cards(use_parent=None):
    """同步扫描本地卡片目录"""
    card_data = {}
    plugin_path = use_parent.app_data_plugin_path
    print(f"plugin_path:{plugin_path}")

    for dir_name in os.listdir(plugin_path):
        dir_path = os.path.join(plugin_path, dir_name)
        config_path = os.path.join(dir_path, 'config.json')
        print(f"config_path:{config_path}")
        if not os.path.isdir(dir_path) or not os.path.exists(config_path):
            continue
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                print(f"config:{config}")
                name = config["name"]
                version = config["version"]

                # 只保留最新版本
                if name in card_data:
                    if version > card_data[name]["version"]:
                        card_data[name] = {"version": version, "path": str(dir_path)}
                else:
                    card_data[name] = {"version": version, "path": str(dir_path)}
        except Exception as e:
            print(f"Error reading {config_path}: {str(e)}")

    return card_data
