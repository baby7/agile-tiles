
update_map_info = {
    "v1.0.0": [
        "提交第一个版本",
    ],
    "v1.1.0": [
        "进行代码签名避免被杀软误报",
        "调整软件图标，托盘图标取消设置颜色功能",
        "增加推广邀请码功能",
        "增加截图翻译功能，同时增加快捷键截图翻译",
        "歌曲模块的图标增加文字显示",
        "简化密码格式、修改密码提示、将忘记密码的密码改为新密码",
        "翻译模块将有道改为默认，增加回车翻译功能",
        "调整翻译和智能对话上方的次数提示信息",
        "加速图片查看的加载速度，并避免失败",
        "托盘右键的关于我们从浏览器链接改为窗口展示信息",
        "打开卡片商店时增加加载动画",
        "智能对话的智能体部分降低输入框的高度",
        "加入用户交流群按钮从弹窗转为跳转到官网关于页",
        "调整主卡片侧边菜单排列顺序",
        "对于低分辨率做单独的设计布局",
        "隐藏安装时的部分弹窗",
        "修复智能对话之前的对话会重复展示的问题",
        "修复软件安装快完成时会有错误提示弹窗的问题",
        "修复软件托盘图标右键退出失效的问题",
        "修复音乐卡片点击进度条闪退的问题",
        "修复判断占用快捷键时占用的可能是本身的问题",
        "修复待办事项的通知未触发的问题",
    ],
}

update_map_date = {
    "v1.0.0": "2025-08-05",
    "v1.1.0": "2025-08-17",
}


def get_update_info():
    update_info = ""
    # 提取所有版本号并排序（从新到旧）
    sorted_versions = sorted(
        update_map_info.keys(),
        key=lambda v: tuple(map(int, v[1:].split('.'))),  # 将 "v0.3.2" 转换为 (0,3,2)
        reverse=True  # 降序排列（最新在前）
    )

    for version in sorted_versions:
        update_info += "## " + version + ":\n"
        for item in update_map_info[version]:
            if item:  # 跳过空字符串
                update_info += "* " + item + "\n"
        update_info += "\n"
    return update_info


def get_current_version():
    return list(update_map_info.keys())[-1]


def gen_download_history_md():
    # 提取所有版本号并排序（从新到旧）
    sorted_versions = sorted(
        update_map_info.keys(),
        key=lambda v: tuple(map(int, v[1:].split('.'))),  # 将 "v0.3.2" 转换为 (0,3,2)
        reverse=True  # 降序排列（最新在前）
    )
    update_info = ""
    for version in sorted_versions:
        update_info += "#### 版本 " + version + " - " + update_map_date[version] + "\n"
        for item in update_map_info[version]:
            if item:  # 跳过空字符串
                update_info += "- " + item + "\n"
        update_info += "\n"
    return update_info

# print(gen_download_history_md())
