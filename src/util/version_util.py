def compare_versions(version_a: str, version_b: str) -> int:
    """
    版本号对比函数（语义化版本规范）

    参数：
    version_a : str - 版本号字符串（示例："v1.2.3" 或 "0.5.1"）
    version_b : str - 版本号字符串

    返回值：
    int - 1: a > b, 0: a == b, -1: a < b
    """
    # 标准化版本格式（移除v前缀和空白）
    def normalize(v: str) -> list:
        return list(
            map(int,
                v.lower().lstrip('v').strip().split('.'))
        )
    a_parts = normalize(version_a)
    b_parts = normalize(version_b)
    # 补零对齐长度
    max_len = max(len(a_parts), len(b_parts))
    a_parts += [0] * (max_len - len(a_parts))
    b_parts += [0] * (max_len - len(b_parts))
    # 逐级比较
    for a, b in zip(a_parts, b_parts):
        if a > b:
            return 1
        elif a < b:
            return -1
    return 0