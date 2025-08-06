import os
import sys


def print_tree(start_path, indent='', prefix=''):
    """递归打印目录树结构"""
    if not os.path.isdir(start_path):
        print(f"{indent}{prefix} [Not a directory]")
        return

    # 获取目录名并打印
    base_name = os.path.basename(start_path)
    if not base_name:
        base_name = start_path  # 处理根目录情况
    print(f"{indent}{prefix}{base_name}/")

    new_indent = indent + '    '
    try:
        entries = sorted(os.listdir(start_path))
    except PermissionError:
        print(f"{new_indent} [Permission Denied]")
        return
    except OSError as e:
        print(f"{new_indent} [Error: {e}]")
        return

    for i, entry in enumerate(entries):
        full_path = os.path.join(start_path, entry)
        is_last = (i == len(entries) - 1)
        new_prefix = '└── ' if is_last else '├── '

        if os.path.isdir(full_path):
            # 递归处理子目录
            print_tree(full_path, indent + ('    ' if is_last else '│   '), new_prefix)
        else:
            # 处理文件/符号链接
            link_target = ''
            if os.path.islink(full_path):
                try:
                    link_target = f" -> {os.readlink(full_path)}"
                except OSError:
                    link_target = " -> [Invalid Link]"
            print(f"{indent}{'│   ' if not is_last else '    '}{new_prefix}{entry}{link_target}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    abs_path = os.path.abspath(path)
    print(f"Directory tree for: {abs_path}")
    print_tree(abs_path)