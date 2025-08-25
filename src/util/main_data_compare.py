def card_has_change(old_data, new_data):
    """
    判断卡片是否有新增、删除、位置改变
    :param old_data: 更新前的数据
    :param new_data: 更新后的数据
    """
    # 判断宽度是否改变
    if "width" in old_data and "width" in new_data:
        old_big_card_width = old_data["width"]
        new_big_card_width = new_data["width"]
        if old_big_card_width != new_big_card_width:
            return True
    else:
        return True

    # 判断高度是否改变
    if "height" in old_data and "height" in new_data:
        old_big_card_height = old_data["height"]
        new_big_card_height = new_data["height"]
        if old_big_card_height != new_big_card_height:
            return True
    else:
        return True

    # 判断普通卡片数量是否相等
    old_normal_card_list = old_data["card"]
    new_normal_card_list = new_data["card"]
    if len(old_normal_card_list) != len(new_normal_card_list):
        return True
    # 判断主要卡片数量是否相等
    old_big_card_list = old_data["bigCard"]
    new_big_card_list = new_data["bigCard"]
    if len(old_big_card_list) != len(new_big_card_list):
        return True

    def compare_card_lists(list1, list2):
        """
        判断两个卡片列表是否相同
        """
        # 检查列表长度（卡片数量）
        if len(list1) != len(list2):
            return False

        # 创建列表的深拷贝以避免修改原始数据
        list1 = [dict(card) for card in list1]
        list2 = [dict(card) for card in list2]

        # 检查每张卡片是否在另一个列表中存在完全匹配项
        for card1 in list1[:]:  # 使用切片复制进行迭代
            found = False
            for card2 in list2[:]:
                # 比较五个关键属性
                if (card1.get('name') == card2.get('name') and
                        card1.get('size') == card2.get('size') and
                        card1.get('x') == card2.get('x') and
                        card1.get('y') == card2.get('y') and
                        card1.get('data') == card2.get('data')):
                    # 找到匹配项后移除已匹配的卡片
                    list1.remove(card1)
                    list2.remove(card2)
                    found = True
                    break

            if not found:
                return False

        return True

    # 判断普通卡片是否改变
    if compare_card_lists(old_normal_card_list, new_normal_card_list):
        return True
    # 判断主要卡片是否改变
    if compare_card_lists(old_big_card_list, new_big_card_list):
        return True
    return False


def get_card_list_by_data_change(old_data, new_data):
    """
    获取有改变的卡片列表
    :param old_data: 更新前的数据
    :param new_data: 更新后的数据
    """

    def compare_big_card_lists(list1, list2):
        """
        获取两个主要卡片有新增、删除、修改的列表
        """
        # 创建唯一标识符集合
        set1 = {(card['name'], card['size']) for card in list1}
        set2 = {(card['name'], card['size']) for card in list2}

        # 计算删除和新增的卡片（基于完整属性）
        del_keys = set1 - set2
        add_keys = set2 - set1

        # 获取完整的卡片对象
        del_list = [card for card in list1 if (card['name'], card['size']) in del_keys]
        add_list = [card for card in list2 if (card['name'], card['size']) in add_keys]

        # 按名称分组
        del_dict = {}
        for card in del_list:
            del_dict.setdefault(card['name'], []).append(card)

        add_dict = {}
        for card in add_list:
            add_dict.setdefault(card['name'], []).append(card)

        # 处理修改的卡片（同名卡片配对）
        modified = []
        common_names = set(del_dict.keys()) & set(add_dict.keys())

        for name in common_names:
            # 获取同名的删除和新增卡片
            del_cards = del_dict[name]
            add_cards = add_dict[name]

            # 按位置和大小排序
            del_sorted = sorted(del_cards, key=lambda c: (c['size']))
            add_sorted = sorted(add_cards, key=lambda c: (c['size']))

            # 配对数量取最小值
            n = min(len(del_sorted), len(add_sorted))

            # 检查配对卡片是否有属性变化
            for i in range(n):
                old_card = del_sorted[i]
                new_card = add_sorted[i]

                if (old_card['size'] != new_card['size']):
                    modified.append({
                        'name': name,
                        'old': {
                            'size': old_card['size']
                        },
                        'new': {
                            'size': new_card['size']
                        }
                    })

            # 更新分组字典
            del_dict[name] = del_sorted[n:]
            add_dict[name] = add_sorted[n:]

        # 收集剩余的删除和新增卡片
        removed = [card for cards in del_dict.values() for card in cards]
        added = [card for cards in add_dict.values() for card in cards]

        # 返回所有差异
        return added + removed + modified

    def compare_normal_card_lists(list1, list2):
        """
        获取两个卡片有新增、删除、修改的列表
        """
        # 创建唯一标识符集合
        set1 = {(card['name'], card['size'], card['x'], card['y']) for card in list1}
        set2 = {(card['name'], card['size'], card['x'], card['y']) for card in list2}

        # 计算删除和新增的卡片（基于完整属性）
        del_keys = set1 - set2
        add_keys = set2 - set1

        # 获取完整的卡片对象
        del_list = [card for card in list1 if (card['name'], card['size'], card['x'], card['y']) in del_keys]
        add_list = [card for card in list2 if (card['name'], card['size'], card['x'], card['y']) in add_keys]

        # 按名称分组
        del_dict = {}
        for card in del_list:
            del_dict.setdefault(card['name'], []).append(card)

        add_dict = {}
        for card in add_list:
            add_dict.setdefault(card['name'], []).append(card)

        # 处理修改的卡片（同名卡片配对）
        modified = []
        common_names = set(del_dict.keys()) & set(add_dict.keys())

        for name in common_names:
            # 获取同名的删除和新增卡片
            del_cards = del_dict[name]
            add_cards = add_dict[name]

            # 按位置和大小排序
            del_sorted = sorted(del_cards, key=lambda c: (c['x'], c['y'], c['size']))
            add_sorted = sorted(add_cards, key=lambda c: (c['x'], c['y'], c['size']))

            # 配对数量取最小值
            n = min(len(del_sorted), len(add_sorted))

            # 检查配对卡片是否有属性变化
            for i in range(n):
                old_card = del_sorted[i]
                new_card = add_sorted[i]

                if (old_card['size'] != new_card['size'] or
                        old_card['x'] != new_card['x'] or
                        old_card['y'] != new_card['y']):
                    modified.append({
                        'name': name,
                        'old': {
                            'size': old_card['size'],
                            'x': old_card['x'],
                            'y': old_card['y']
                        },
                        'new': {
                            'size': new_card['size'],
                            'x': new_card['x'],
                            'y': new_card['y']
                        }
                    })

            # 更新分组字典
            del_dict[name] = del_sorted[n:]
            add_dict[name] = add_sorted[n:]

        # 收集剩余的删除和新增卡片
        removed = [card for cards in del_dict.values() for card in cards]
        added = [card for cards in add_dict.values() for card in cards]

        # 返回所有差异
        return added + removed + modified

    def compare_config_data(old_config, new_config):
        """
        比较配置数据的变化
        :param old_config: 旧配置数据
        :param new_config: 新配置数据
        :return: 配置变化字典 {配置项名称: 变化详情}
        """
        changes = {}

        # 获取所有配置键名
        old_keys = set(old_config.keys())
        new_keys = set(new_config.keys())

        # 1. 检查新增的配置键
        for key in new_keys - old_keys:
            changes[key] = {
                "type": "added",
                "data": new_config[key]
            }

        # 2. 检查删除的配置键
        for key in old_keys - new_keys:
            changes[key] = {
                "type": "removed",
                "data": old_config[key]
            }

        # 3. 检查修改的配置键
        for key in old_keys & new_keys:
            old_value = old_config[key]
            new_value = new_config[key]

            # 深度比较两个字典是否相等
            if old_value != new_value:
                changes[key] = {
                    "type": "modified",
                    "old_data": old_value,
                    "new_data": new_value
                }
        print(f"changes:{changes}")

        return changes

    # 获取有修改的普通卡片列表
    old_normal_card_list = old_data["card"]
    new_normal_card_list = new_data["card"]
    normal_card_data_update_list = compare_normal_card_lists(old_normal_card_list, new_normal_card_list)

    # 获取有修改的主要卡片列表
    old_big_card_list = old_data["bigCard"]
    new_big_card_list = new_data["bigCard"]
    big_card_data_update_list = compare_big_card_lists(old_big_card_list, new_big_card_list)

    # 比较配置数据的变化
    old_config_data = old_data.get("data", {})
    new_config_data = new_data.get("data", {})
    enduring_changes = compare_config_data(old_config_data, new_config_data)

    # 返回布局变化和配置变化
    return normal_card_data_update_list, big_card_data_update_list, enduring_changes


def setting_keyboard_has_change(old_data, new_data):
    """
    快捷键是否有更新
    :param old_data: 更新前的数据
    :param new_data: 更新后的数据
    """
    old_setting = old_data["data"]["SettingCard"]
    new_setting = new_data["data"]["SettingCard"]
    setting_key_list = ["wakeUpByKeyboard", "wakeUpByKeyboardType",
                        "screenshotByKeyboard", "screenshotByKeyboardType",
                        "searchByKeyboard", "searchByKeyboardType"]
    for setting_key in setting_key_list:
        if old_setting.get(setting_key) != new_setting.get(setting_key):
            return True
    return False


def setting_has_change(old_data, new_data):
    """
    设置数据是否有更新
    :param old_data: 更新前的数据
    :param new_data: 更新后的数据
    """
    old_setting = old_data["data"]["SettingCard"]
    new_setting = new_data["data"]["SettingCard"]
    setting_key_list = ["theme", "themeMode", "themeTransparency",
                        "wakeUpByKeyboard", "wakeUpByKeyboardType",
                        "screenshotByKeyboard", "screenshotByKeyboardType",
                        "searchByKeyboard", "searchByKeyboardType",
                        "screenName", "windowPosition", "formAnimationType", "formAnimationTime", "wakeUpByMouse",
                        "wakeUpByMouseTime", "wakeUpByMouseHide", "menuPosition", "fontName", "messageNotification",
                        "autoUpdate"]
    for setting_key in setting_key_list:
        if old_setting.get(setting_key) != new_setting.get(setting_key):
            return True
    return False


def setting_screen_has_change(old_data, new_data):
    """
    设置数据中的屏幕数据是否有更新
    :param old_data: 更新前的数据
    :param new_data: 更新后的数据
    """
    old_setting = old_data["data"]["SettingCard"]
    new_setting = new_data["data"]["SettingCard"]
    setting_key_list = ["screenName", "windowPosition", "formAnimationType", "formAnimationTime", "wakeUpByMouse",
                        "wakeUpByMouseTime", "wakeUpByMouseHide", "menuPosition", "fontName"]
    for setting_key in setting_key_list:
        if old_setting.get(setting_key) != new_setting.get(setting_key):
            return True
    return False


def setting_system_has_change(old_data, new_data):
    """
    设置数据中的系统数据是否有更新
    :param old_data: 更新前的数据
    :param new_data: 更新后的数据
    """
    old_setting = old_data["data"]["SettingCard"]
    new_setting = new_data["data"]["SettingCard"]
    setting_key_list = ["wakeUpByKeyboard", "wakeUpByKeyboardType",
                        "screenshotByKeyboard", "screenshotByKeyboardType",
                        "searchByKeyboard", "searchByKeyboardType"]
    for setting_key in setting_key_list:
        if old_setting.get(setting_key) != new_setting.get(setting_key):
            return True
    return False


def setting_theme_has_change(old_data, new_data):
    """
    设置数据中的屏幕数据是否有更新
    :param old_data: 更新前的数据
    :param new_data: 更新后的数据
    """
    old_setting = old_data["data"]["SettingCard"]
    new_setting = new_data["data"]["SettingCard"]
    setting_key_list = ["theme", "themeMode", "themeTransparency"]
    for setting_key in setting_key_list:
        if old_setting.get(setting_key) != new_setting.get(setting_key):
            return True
    return False
