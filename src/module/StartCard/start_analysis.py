def analyze_card_list(user_card_list, cloud_card_list, local_card_list):
    delete_list = []
    download_list = []

    # # 1. 找出需要删除的卡片（本地有但用户不需要）
    # for card_name in local_card_list:
    #     if card_name not in user_card_list:
    #         delete_list.append(card_name)

    # 2. 找出需要下载/更新的卡片
    for card_name in user_card_list:
        # 剔除MainCard
        if card_name == "MainCard":
            continue

        # 用户需要但本地没有
        if card_name not in local_card_list:
            if card_name in cloud_card_list:
                download_list.append(card_name)
            continue

        # 检查版本更新
        # local_version = local_card_list[card_name]["version"]
        # cloud_version = cloud_card_list[card_name]["currentVersion"]["version"]
        # if cloud_version > local_version:
        #     download_list.append(card_name)
        #     # 旧版本加入删除列表
        #     if card_name not in delete_list:
        #         delete_list.append(card_name)

    return delete_list, download_list