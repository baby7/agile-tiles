import os
import time
import ctypes
from ctypes import wintypes
import datetime
import subprocess
import psutil
from PySide6.QtCore import QThread, Signal


class EverythingResult:
    """Everything搜索结果类"""

    def __init__(self, size, date_modified, filename, path):
        self.size = size
        self.date_modified = date_modified
        self.filename = filename
        self.path = path

    @property
    def is_folder(self):
        return self.size < 0

    def __str__(self):
        size_str = "(文件夹)" if self.is_folder else f"{self.size} B"
        return f"{self.filename} ({size_str}) - {self.date_modified:%Y-%m-%d %H:%M:%S}"


class EverythingSearcher:
    """Everything搜索器"""
    # API常量
    EVERYTHING_OK = 0
    EVERYTHING_ERROR_MEMORY = 1
    EVERYTHING_ERROR_IPC = 2
    EVERYTHING_ERROR_REGISTERCLASSEX = 3
    EVERYTHING_ERROR_CREATEWINDOW = 4
    EVERYTHING_ERROR_CREATETHREAD = 5
    EVERYTHING_ERROR_INVALIDINDEX = 6
    EVERYTHING_ERROR_INVALIDCALL = 7

    # 请求标志
    EVERYTHING_REQUEST_FILE_NAME = 0x00000001
    EVERYTHING_REQUEST_PATH = 0x00000002
    EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME = 0x00000004
    EVERYTHING_REQUEST_EXTENSION = 0x00000008
    EVERYTHING_REQUEST_SIZE = 0x00000010
    EVERYTHING_REQUEST_DATE_CREATED = 0x00000020
    EVERYTHING_REQUEST_DATE_MODIFIED = 0x00000040
    EVERYTHING_REQUEST_DATE_ACCESSED = 0x00000080
    EVERYTHING_REQUEST_ATTRIBUTES = 0x00000100
    EVERYTHING_REQUEST_FILE_LIST_FILE_NAME = 0x00000200
    EVERYTHING_REQUEST_RUN_COUNT = 0x00000400
    EVERYTHING_REQUEST_DATE_RUN = 0x00000800
    EVERYTHING_REQUEST_DATE_RECENTLY_CHANGED = 0x00001000
    EVERYTHING_REQUEST_HIGHLIGHTED_FILE_NAME = 0x00002000
    EVERYTHING_REQUEST_HIGHLIGHTED_PATH = 0x00004000
    EVERYTHING_REQUEST_HIGHLIGHTED_FULL_PATH_AND_FILE_NAME = 0x00008000

    # 排序标志
    EVERYTHING_SORT_NAME_ASCENDING = 1
    EVERYTHING_SORT_NAME_DESCENDING = 2
    EVERYTHING_SORT_PATH_ASCENDING = 3
    EVERYTHING_SORT_PATH_DESCENDING = 4
    EVERYTHING_SORT_SIZE_ASCENDING = 5
    EVERYTHING_SORT_SIZE_DESCENDING = 6
    EVERYTHING_SORT_EXTENSION_ASCENDING = 7
    EVERYTHING_SORT_EXTENSION_DESCENDING = 8
    EVERYTHING_SORT_TYPE_NAME_ASCENDING = 9
    EVERYTHING_SORT_TYPE_NAME_DESCENDING = 10
    EVERYTHING_SORT_DATE_CREATED_ASCENDING = 11
    EVERYTHING_SORT_DATE_CREATED_DESCENDING = 12
    EVERYTHING_SORT_DATE_MODIFIED_ASCENDING = 13
    EVERYTHING_SORT_DATE_MODIFIED_DESCENDING = 14
    EVERYTHING_SORT_ATTRIBUTES_ASCENDING = 15
    EVERYTHING_SORT_ATTRIBUTES_DESCENDING = 16
    EVERYTHING_SORT_FILE_LIST_FILENAME_ASCENDING = 17
    EVERYTHING_SORT_FILE_LIST_FILENAME_DESCENDING = 18
    EVERYTHING_SORT_RUN_COUNT_ASCENDING = 19
    EVERYTHING_SORT_RUN_COUNT_DESCENDING = 20
    EVERYTHING_SORT_DATE_RECENTLY_CHANGED_ASCENDING = 21
    EVERYTHING_SORT_DATE_RECENTLY_CHANGED_DESCENDING = 22
    EVERYTHING_SORT_DATE_ACCESSED_ASCENDING = 23
    EVERYTHING_SORT_DATE_ACCESSED_DESCENDING = 24
    EVERYTHING_SORT_DATE_RUN_ASCENDING = 25
    EVERYTHING_SORT_DATE_RUN_DESCENDING = 26

    def __init__(self, everything_path=None):
        self.everything_path = everything_path
        self.dll = None
        self._load_dll()
        self._setup_function_prototypes()
        self._ensure_everything_running()

    def _find_everything_path(self):
        """查找Everything安装路径"""
        # 如果提供了自定义路径，使用它
        if self.everything_path and os.path.exists(self.everything_path):
            return self.everything_path

        # 尝试默认路径
        if os.path.exists(os.path.join(self.everything_path or "", "Everything64.dll")):
            return self.everything_path or ""

        # 尝试常见安装位置
        common_paths = [
            os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), 'Everything'),
            os.path.join(os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'), 'Everything'),
            "C:\\Everything"
        ]

        for path in common_paths:
            if os.path.exists(os.path.join(path, "Everything64.dll")):
                return path

        raise RuntimeError(
            "Everything not found. Please install Everything or provide the path to the Everything directory.")

    def _load_dll(self):
        """加载Everything DLL"""
        try:
            # 尝试加载Everything64.dll
            dll_path = os.path.join(self.everything_path or "", "Everything64.dll")
            self.dll = ctypes.WinDLL(dll_path)
        except OSError:
            try:
                # 尝试加载Everything32.dll
                dll_path = os.path.join(self.everything_path or "", "Everything32.dll")
                self.dll = ctypes.WinDLL(dll_path)
            except OSError:
                # 尝试在系统路径中查找
                try:
                    self.dll = ctypes.WinDLL("Everything64.dll")
                except OSError:
                    try:
                        self.dll = ctypes.WinDLL("Everything32.dll")
                    except OSError:
                        raise RuntimeError("Everything DLL not found. Please install Everything.")

    def _is_everything_process_running(self):
        """检查Everything进程是否正在运行"""
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and proc.info['name'].lower() == 'everything.exe':
                    return True
            return False
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return False

    def _is_everything_service_ready(self):
        """检查Everything服务是否就绪"""
        if not self.dll:
            return False

        try:
            # 尝试一个简单的API调用来检查服务状态
            error_code = self.dll.Everything_GetLastError()
            # 如果返回IPC错误，说明服务未运行
            return error_code != self.EVERYTHING_ERROR_IPC
        except:
            return False

    def _ensure_everything_running(self):
        """确保Everything正在运行"""
        # 检查进程是否在运行
        process_running = self._is_everything_process_running()

        # 检查服务是否就绪
        service_ready = False
        if process_running:
            # 如果进程在运行，检查服务状态
            service_ready = self._is_everything_service_ready()

        # 如果服务未就绪，启动Everything
        if not service_ready:
            self._start_everything_service()

            # 等待服务启动
            for _ in range(20):  # 最多等待10秒
                time.sleep(0.5)
                if self._is_everything_service_ready():
                    break

    def _start_everything_service(self):
        """启动Everything服务"""
        # 查找Everything.exe路径
        everything_path = self._find_everything_path()
        exe_path = os.path.join(everything_path, "Everything.exe")

        if not os.path.exists(exe_path):
            raise RuntimeError("Everything.exe not found.")

        try:
            # 使用subprocess启动Everything，并隐藏窗口
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0  # SW_HIDE

            subprocess.Popen(
                [exe_path, "-startup"],
                startupinfo=startupinfo,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception as e:
            raise RuntimeError(f"Failed to start Everything: {e}")

    def _setup_function_prototypes(self):
        """设置DLL函数原型"""
        # 设置搜索字符串
        self.dll.Everything_SetSearchW.argtypes = [wintypes.LPCWSTR]
        self.dll.Everything_SetSearchW.restype = wintypes.DWORD

        # 设置请求标志
        self.dll.Everything_SetRequestFlags.argtypes = [wintypes.DWORD]
        self.dll.Everything_SetRequestFlags.restype = None

        # 执行查询
        self.dll.Everything_QueryW.argtypes = [wintypes.BOOL]
        self.dll.Everything_QueryW.restype = wintypes.BOOL

        # 设置排序
        self.dll.Everything_SetSort.argtypes = [wintypes.DWORD]
        self.dll.Everything_SetSort.restype = None

        # 获取结果数量
        self.dll.Everything_GetNumResults.argtypes = []
        self.dll.Everything_GetNumResults.restype = wintypes.DWORD

        # 获取完整路径名
        self.dll.Everything_GetResultFullPathNameW.argtypes = [
            wintypes.DWORD,  # nIndex
            wintypes.LPWSTR,  # lpString
            wintypes.DWORD  # nMaxCount
        ]
        self.dll.Everything_GetResultFullPathNameW.restype = None

        # 获取修改日期
        self.dll.Everything_GetResultDateModified.argtypes = [
            wintypes.DWORD,  # nIndex
            ctypes.POINTER(ctypes.c_longlong)  # lpFileTime
        ]
        self.dll.Everything_GetResultDateModified.restype = wintypes.BOOL

        # 获取文件大小
        self.dll.Everything_GetResultSize.argtypes = [
            wintypes.DWORD,  # nIndex
            ctypes.POINTER(ctypes.c_longlong)  # lpFileSize
        ]
        self.dll.Everything_GetResultSize.restype = wintypes.BOOL

        # 获取文件名
        self.dll.Everything_GetResultFileNameW.argtypes = [wintypes.DWORD]
        self.dll.Everything_GetResultFileNameW.restype = ctypes.c_void_p

        # 重置搜索
        self.dll.Everything_Reset.argtypes = []
        self.dll.Everything_Reset.restype = None

        # 获取错误信息
        self.dll.Everything_GetLastError.argtypes = []
        self.dll.Everything_GetLastError.restype = wintypes.DWORD

        # 检查数据库是否已加载
        self.dll.Everything_IsDBLoaded.argtypes = []
        self.dll.Everything_IsDBLoaded.restype = wintypes.BOOL

        # 设置偏移量和最大结果数（用于分页）
        self.dll.Everything_SetOffset.argtypes = [wintypes.DWORD]
        self.dll.Everything_SetOffset.restype = None

        self.dll.Everything_SetMax.argtypes = [wintypes.DWORD]
        self.dll.Everything_SetMax.restype = None

        # 获取总结果数
        if hasattr(self.dll, 'Everything_GetTotResults'):
            self.dll.Everything_GetTotResults.argtypes = []
            self.dll.Everything_GetTotResults.restype = wintypes.DWORD

    def is_db_loaded(self):
        """检查数据库是否已加载"""
        return self.dll.Everything_IsDBLoaded()

    def get_last_error(self):
        """获取最后错误代码"""
        return self.dll.Everything_GetLastError()

    def search(self, query, offset=0, max_results=100):
        """执行搜索"""
        # 确保Everything正在运行
        self._ensure_everything_running()

        # 设置搜索查询
        error_code = self.dll.Everything_SetSearchW(query)
        if error_code != self.EVERYTHING_OK:
            raise RuntimeError(f"Everything search error: {error_code}")

        # 设置请求标志
        request_flags = (self.EVERYTHING_REQUEST_FILE_NAME |
                         self.EVERYTHING_REQUEST_PATH |
                         self.EVERYTHING_REQUEST_DATE_MODIFIED |
                         self.EVERYTHING_REQUEST_SIZE)
        self.dll.Everything_SetRequestFlags(request_flags)

        # 设置偏移量和最大结果数
        self.dll.Everything_SetOffset(offset)
        self.dll.Everything_SetMax(max_results)

        # 设置排序
        self.dll.Everything_SetSort(self.EVERYTHING_SORT_NAME_DESCENDING)

        # 执行查询
        if not self.dll.Everything_QueryW(True):  # True表示等待查询完成
            error_code = self.dll.Everything_GetLastError()
            if error_code == self.EVERYTHING_ERROR_IPC:
                raise RuntimeError("Everything service is not running. Please start Everything.")
            else:
                raise RuntimeError(f"Everything query error: {error_code}")

        # 获取结果数量
        result_count = self.dll.Everything_GetNumResults()

        # 获取总结果数（如果可用）
        if hasattr(self.dll, 'Everything_GetTotResults'):
            total_results = self.dll.Everything_GetTotResults()
        else:
            total_results = result_count  # 如果没有获取总结果数的函数，使用当前结果数

        # 收集结果
        results = []
        for i in range(result_count):
            # 获取完整路径
            path_buffer = ctypes.create_unicode_buffer(260)
            self.dll.Everything_GetResultFullPathNameW(i, path_buffer, ctypes.sizeof(path_buffer))
            path = path_buffer.value

            # 获取修改日期
            date_modified = ctypes.c_longlong()
            if self.dll.Everything_GetResultDateModified(i, ctypes.byref(date_modified)):
                # 将Windows文件时间转换为datetime
                dt = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=date_modified.value // 10)
            else:
                dt = datetime.datetime.min

            # 获取文件大小
            size = ctypes.c_longlong()
            if not self.dll.Everything_GetResultSize(i, ctypes.byref(size)):
                size.value = -1  # 表示文件夹

            # 获取文件名
            filename_ptr = self.dll.Everything_GetResultFileNameW(i)
            filename = ctypes.wstring_at(filename_ptr)

            results.append(EverythingResult(
                size=size.value,
                date_modified=dt,
                filename=filename,
                path=path
            ))

        # 重置搜索状态
        self.dll.Everything_Reset()

        has_more = (offset + result_count) < total_results if hasattr(self.dll, 'Everything_GetTotResults') else False

        return results, total_results, has_more


class EverythingStatusThread(QThread):
    """Everything状态检查线程"""
    status_updated = Signal(str, bool)  # 状态消息, 是否就绪
    error_occurred = Signal(str)

    def __init__(self, everything_path=None, parent=None):
        super().__init__(parent)
        self.everything_path = everything_path
        self._is_running = True

    def run(self):
        try:
            # 创建Everything搜索器
            searcher = EverythingSearcher(self.everything_path)

            # 检查数据库是否已加载
            if not searcher.is_db_loaded():
                self.status_updated.emit("Everything正在索引文件，请稍候...", False)

                # 等待数据库加载完成
                for _ in range(60):  # 最多等待30秒
                    if not self._is_running:
                        return
                    time.sleep(0.5)
                    if searcher.is_db_loaded():
                        self.status_updated.emit("Everything已就绪", True)
                        return

                self.status_updated.emit("Everything索引超时，可能仍在索引中", False)
            else:
                self.status_updated.emit("Everything已就绪", True)

        except Exception as e:
            self.error_occurred.emit(str(e))

    def stop(self):
        self._is_running = False
        self.wait()


class EverythingSearchThread(QThread):
    """Everything搜索线程"""
    search_finished = Signal(list, int, bool)  # 结果列表, 总结果数, 是否还有更多结果
    search_error = Signal(str)
    indexing_status = Signal(bool)  # True表示正在索引，False表示索引完成

    def __init__(self, search_text, everything_path=None, offset=0, limit=50, parent=None):
        super().__init__(parent)
        self.search_text = search_text
        self.everything_path = everything_path
        self.offset = offset
        self.limit = limit
        self._is_running = True

    def run(self):
        try:
            # 创建Everything搜索器
            searcher = EverythingSearcher(self.everything_path)

            # 检查数据库是否已加载
            if not searcher.is_db_loaded():
                self.indexing_status.emit(True)
                # 等待数据库加载完成
                for _ in range(30):  # 最多等待15秒
                    if not self._is_running:
                        return
                    time.sleep(0.5)
                    if searcher.is_db_loaded():
                        break
                self.indexing_status.emit(False)

            if not self._is_running:
                return

            # 执行搜索
            results, total_results, has_more = searcher.search(
                self.search_text,
                offset=self.offset,
                max_results=self.limit
            )

            if not self._is_running:
                return

            # 发送结果
            self.search_finished.emit(results, total_results, has_more)

        except Exception as e:
            self.search_error.emit(str(e))

    def stop(self):
        self._is_running = False
        self.wait()
