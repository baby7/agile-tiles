import hashlib
import platform
import subprocess
import re


def get_hardware_id():
    """获取基于硬件信息的唯一标识（SHA256哈希值）"""
    system_info = ""

    try:
        # 获取操作系统类型
        os_name = platform.system()

        # Windows系统
        if os_name == "Windows":
            import wmi
            c = wmi.WMI()

            # 主板信息
            for board in c.Win32_BaseBoard():
                if board.SerialNumber:
                    system_info += f"MB:{board.SerialNumber.strip()};"

            # BIOS信息
            for bios in c.Win32_BIOS():
                if bios.SerialNumber:
                    system_info += f"BIOS:{bios.SerialNumber.strip()};"

            # 硬盘序列号（第一块硬盘）
            for disk in c.Win32_DiskDrive(Index=0):
                if disk.SerialNumber:
                    system_info += f"DISK:{disk.SerialNumber.strip()};"

        # Linux系统
        elif os_name == "Linux":
            # 获取主板UUID
            try:
                with open("/sys/class/dmi/id/product_uuid", "r") as f:
                    system_info += f"MBUUID:{f.read().strip()};"
            except:
                pass

            # 获取机器ID（现代Linux系统）
            for path in ["/etc/machine-id", "/var/lib/dbus/machine-id"]:
                try:
                    with open(path, "r") as f:
                        system_info += f"MACHINE_ID:{f.read().strip()};"
                    break
                except:
                    continue

        # macOS系统
        elif os_name == "Darwin":
            # 获取硬件序列号
            result = subprocess.run(
                ["ioreg", "-c", "IOPlatformExpertDevice", "-d", "2"],
                capture_output=True,
                text=True
            )
            match = re.search(r'"IOPlatformSerialNumber" = "([^"]+)"', result.stdout)
            if match:
                system_info += f"SERIAL:{match.group(1)};"

            # 获取硬件UUID
            result = subprocess.run(
                ["system_profiler", "SPHardwareDataType"],
                capture_output=True,
                text=True
            )
            match = re.search(r"Hardware UUID: ([\w-]+)", result.stdout)
            if match:
                system_info += f"UUID:{match.group(1)};"

        # 如果以上方法均失败，使用平台默认标识
        if not system_info:
            system_info = platform.node()  # 主机名（作为后备方案）

    except Exception as e:
        # 异常时使用平台标识作为后备
        system_info = platform.node()

    # 生成SHA256哈希值（固定长度64字符）
    return hashlib.sha256(system_info.encode()).hexdigest()


# 使用示例
# if __name__ == "__main__":
#     machine_id = get_hardware_id()
#     print(f"本机唯一标识: {machine_id}")