import os
import json
from pathlib import Path

def scan_local_cards():
    """同步扫描本地卡片目录"""
    card_data = {}
    plugin_path = Path("./plugin")
    print(f"plugin_path:{plugin_path}")

    if plugin_path.exists():
        for dir_path in plugin_path.iterdir():
            config_path = dir_path / "config.json"
            print(f"config_path:{config_path}")
            if config_path.exists():
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
