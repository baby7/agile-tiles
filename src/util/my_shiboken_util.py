from PySide6.QtCore import QObject


def is_qobject_valid(obj: QObject) -> bool:
    """
    综合判断QObject是否有效的工具函数

    Args:
        obj: 要检测的QObject或其子类对象

    Returns:
        bool: True表示对象有效，False表示对象无效或已被删除
    """
    # 1. 检查Python引用是否存在
    if obj is None:
        return False

    # # 2. 使用shiboken6检查底层C++对象
    # if not my_shiboken_util.is_qobject_valid(obj):
    #     return False

    # 3. 可选：通过尝试访问简单属性进行双重验证
    try:
        # 尝试访问一个简单的属性，如果底层对象被删除会抛出RuntimeError
        _ = obj.objectName()
        return True
    except RuntimeError as e:
        if "Internal C++ object" in str(e):
            return False
        else:
            # 其他RuntimeError，重新抛出
            raise e
