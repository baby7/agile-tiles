import os
import traceback
import json
import cgi
from http.server import BaseHTTPRequestHandler
from urllib.parse import unquote, quote


class HttpServerHandler(BaseHTTPRequestHandler):
    """自定义HTTP请求处理器"""

    def __init__(self, *args, **kwargs):
        self.base_path = None
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # 处理中文路径解码
        path = unquote(self.path)

        # 如果是根路径，返回文件列表
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # 生成HTML页面
            html = self.generate_file_list()
            self.wfile.write(html.encode('utf-8'))
            return

        # 处理文本内容请求
        if path.startswith('/text/'):
            try:
                text_id = int(path.split('/')[2])
                text_content = self.server.file_data["texts"][text_id]["content"]

                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(text_content.encode('utf-8'))
                return
            except (IndexError, ValueError):
                traceback.print_exc()
                self.send_error(404, "Text not found")
                return

        # 处理文件或文件夹请求
        if path.startswith('/file/'):
            try:
                # 获取文件路径（去掉/file/前缀）
                file_relative_path = unquote(path[6:])  # 去掉前面的'/file/'

                # 在文件列表中查找
                file_found = False
                file_path = None

                for item in self.server.file_data["files"]:
                    if item["name"] == file_relative_path:
                        file_path = item["path"]
                        file_found = True
                        break

                # 如果没有直接匹配，可能是文件夹内的文件
                if not file_found:
                    # 查找父文件夹
                    parent_folder_name = file_relative_path.split('/')[0]
                    for item in self.server.file_data["files"]:
                        if item["type"] == "folder" and item["name"] == parent_folder_name:
                            # 构建完整路径
                            file_path = os.path.join(item["path"], file_relative_path[len(parent_folder_name) + 1:])
                            if os.path.exists(file_path):
                                file_found = True
                                break

                if not file_found:
                    self.send_error(404, "File not found")
                    return

                if os.path.isdir(file_path):
                    # 如果是目录，显示目录内容
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()

                    html = self.generate_directory_listing(file_path, path)
                    self.wfile.write(html.encode('utf-8'))
                elif os.path.isfile(file_path):
                    # 如果是文件，提供下载
                    self.send_response(200)
                    # 使用正确的编码处理文件名
                    filename = os.path.basename(file_path)
                    try:
                        # 尝试UTF-8编码
                        encoded_filename = quote(filename)
                        content_disposition = f'attachment; filename="{encoded_filename}"'
                    except:
                        # 如果UTF-8失败，使用原始文件名
                        content_disposition = f'attachment; filename="{filename}"'

                    self.send_header('Content-Type', 'application/octet-stream')
                    self.send_header('Content-Disposition', content_disposition)
                    self.send_header('Content-Length', str(os.path.getsize(file_path)))
                    self.end_headers()

                    with open(file_path, 'rb') as f:
                        self.wfile.write(f.read())
                else:
                    self.send_error(404, "File not found")
            except Exception as e:
                traceback.print_exc()
                self.send_error(500, f"Server error: {str(e)}")
            return

        # 如果不是/text/或/file/开头的请求，返回404
        self.send_error(404, "Not found")

    def do_POST(self):
        """处理POST请求，用于文件上传"""
        # 处理中文路径解码
        path = unquote(self.path)

        if path == '/upload/file':
            self.handle_file_upload()
        elif path == '/upload/text':
            self.handle_text_upload()
        else:
            self.send_error(404, "Not found")

    def handle_file_upload(self):
        """处理文件上传"""
        try:
            # 检查内容类型
            content_type = self.headers.get('Content-Type')
            if not content_type or not content_type.startswith('multipart/form-data'):
                self.send_error(400, "Bad Request: expecting multipart/form-data")
                return

            # 解析multipart表单数据
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type']}
            )

            # 获取上传的文件 - 使用更安全的方式检查
            if 'file' not in form:
                self.send_error(400, "Bad Request: no file field in form")
                return

            file_field = form['file']

            # 检查file_field是否有效且包含文件数据
            if not hasattr(file_field, 'file') or not file_field.file:
                self.send_error(400, "Bad Request: no file uploaded")
                return

            # 获取文件名
            filename = file_field.filename
            if not filename:
                self.send_error(400, "Bad Request: no filename provided")
                return

            # 安全地处理文件名
            filename = os.path.basename(filename)
            save_path = os.path.join(self.server.upload_dir, filename)

            # 如果文件已存在，添加数字后缀
            counter = 1
            while os.path.exists(save_path):
                name, ext = os.path.splitext(filename)
                save_path = os.path.join(self.server.upload_dir, f"{name}_{counter}{ext}")
                counter += 1

            # 保存文件
            with open(save_path, 'wb') as f:
                while True:
                    chunk = file_field.file.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)

            # 创建文件信息
            client_ip = self.client_address[0]
            file_info = {
                "name": os.path.basename(save_path),
                "path": save_path,
                "type": "file",
                "size": os.path.getsize(save_path),
                "uploader": client_ip  # 添加上传者IP
            }

            # 添加到文件数据中
            self.server.file_data["files"].append(file_info)

            # 发送成功响应
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({"status": "success", "filename": file_info["name"]})
            self.wfile.write(response.encode('utf-8'))

            # 触发数据更新回调
            if hasattr(self.server, 'update_callback') and self.server.update_callback:
                self.server.update_callback()

        except Exception as e:
            traceback.print_exc()
            self.send_error(500, f"Server error: {str(e)}")

    def handle_text_upload(self):
        """处理文本上传（使用JSON格式）"""
        try:
            # 获取内容长度
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error(400, "Bad Request: no content")
                return

            # 检查内容类型是否为JSON
            content_type = self.headers.get('Content-Type', '')
            if not content_type.startswith('application/json'):
                self.send_error(400, "Bad Request: expecting application/json")
                return

            # 读取POST数据
            post_data = self.rfile.read(content_length)

            # 解析JSON数据
            try:
                data = json.loads(post_data.decode('utf-8'))
                text_content = data.get('text', '')
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                self.send_error(400, f"Bad Request: invalid JSON - {str(e)}")
                return

            if not text_content:
                self.send_error(400, "Bad Request: empty text content")
                return

            # 创建文本信息
            client_ip = self.client_address[0]
            text_info = {
                "content": text_content,
                "type": "text",
                "uploader": client_ip  # 添加上传者IP
            }

            # 添加到文本数据中
            self.server.file_data["texts"].append(text_info)

            # 发送成功响应
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({"status": "success"})
            self.wfile.write(response.encode('utf-8'))

            # 触发数据更新回调
            if hasattr(self.server, 'update_callback') and self.server.update_callback:
                self.server.update_callback()

        except Exception as e:
            traceback.print_exc()
            self.send_error(500, f"Server error: {str(e)}")

    def generate_file_list(self):
        """生成文件列表HTML页面"""
        # 准备文本内容的JSON字符串
        text_contents = []
        for item in self.server.file_data["texts"]:
            # 直接存储原始文本内容
            text_contents.append(item["content"])

        # 使用json.dumps确保正确转义
        texts_json = json.dumps(text_contents, ensure_ascii=False)

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>灵卡面板·局域网文件共享</title>
            <style>
                :root {{
                    --primary-color: #007aff;
                    --primary-hover: #0056b3;
                    --success-color: #34c759;
                    --success-hover: #2ca44e;
                    --background: #f5f5f7;
                    --card-bg: white;
                    --text-color: #333;
                    --text-secondary: #666;
                    --border-color: #eee;
                    --shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}

                * {{
                    box-sizing: border-box;
                }}

                body {{ 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
                    margin: 0; 
                    padding: 20px; 
                    background-color: var(--background); 
                    color: var(--text-color);
                    font-size: 16px;
                    line-height: 1.5;
                }}

                h1 {{ 
                    color: var(--text-color); 
                    margin-top: 0;
                    font-size: 1.8rem;
                }}

                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                }}

                .upload-buttons {{
                    display: flex;
                    gap: 12px;
                    margin-bottom: 20px;
                    flex-wrap: wrap;
                }}

                .action-button {{ 
                    background-color: var(--primary-color);
                    color: white;
                    border: none;
                    padding: 12px 20px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 1rem;
                    min-height: 44px;
                    min-width: 44px;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    transition: background-color 0.2s;
                }}

                .action-button:hover {{ 
                    background-color: var(--primary-hover); 
                }}

                .file-list {{ 
                    background: var(--card-bg); 
                    border-radius: 12px; 
                    padding: 0; 
                    box-shadow: var(--shadow); 
                    overflow: hidden;
                }}

                .file-item {{ 
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 16px; 
                    border-bottom: 1px solid var(--border-color); 
                    flex-wrap: wrap;
                }}

                .file-item:last-child {{ 
                    border-bottom: none; 
                }}

                .file-name {{ 
                    flex-grow: 1;
                    color: var(--primary-color); 
                    text-decoration: none; 
                    cursor: default;
                    margin-bottom: 8px;
                    word-break: break-word;
                }}

                .file-name.folder {{ 
                    font-weight: bold; 
                    cursor: pointer; 
                }}

                .file-name.folder:hover {{ 
                    text-decoration: underline; 
                }}

                .file-info {{
                    font-size: 0.9rem;
                    color: var(--text-secondary);
                    margin: 4px 0;
                    width: 100%;
                }}

                .file-actions {{
                    display: flex;
                    gap: 8px;
                }}

                .modal {{
                    display: none;
                    position: fixed;
                    z-index: 1000;
                    left: 0;
                    top: 0;
                    width: 100%;
                    height: 100%;
                    background-color: rgba(0,0,0,0.5);
                    overflow: auto;
                }}

                .modal-content {{
                    background-color: var(--card-bg);
                    margin: 10% auto;
                    padding: 24px;
                    border-radius: 12px;
                    width: 90%;
                    max-width: 500px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
                    position: relative;
                }}

                .close {{
                    color: #aaa;
                    position: absolute;
                    top: 16px;
                    right: 20px;
                    font-size: 28px;
                    font-weight: bold;
                    cursor: pointer;
                    line-height: 1;
                }}

                .close:hover {{
                    color: black;
                }}

                .upload-form {{ 
                    margin-top: 20px; 
                }}

                .upload-form input[type="file"],
                .upload-form input[type="text"],
                .upload-form textarea {{
                    width: 100%;
                    padding: 12px;
                    margin-bottom: 16px;
                    border: 1px solid #d1d1d6;
                    border-radius: 8px;
                    font-size: 1rem;
                }}

                .upload-form input[type="submit"] {{
                    background-color: var(--success-color);
                    color: white;
                    border: none;
                    padding: 12px 20px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 1rem;
                    min-height: 44px;
                    width: 100%;
                }}

                .upload-form input[type="submit"]:hover {{
                    background-color: var(--success-hover);
                }}

                .back-link {{
                    margin-bottom: 20px; 
                    display: inline-block; 
                    color: var(--primary-color);
                    text-decoration: none;
                    font-size: 1rem;
                    min-height: 44px;
                    display: inline-flex;
                    align-items: center;
                }}

                .back-link:hover {{
                    text-decoration: underline;
                }}

                /* 响应式设计 */
                @media (min-width: 768px) {{
                    body {{
                        padding: 40px;
                    }}

                    .file-item {{
                        flex-wrap: nowrap;
                    }}

                    .file-info {{
                        width: auto;
                        margin-left: 10px;
                        margin-bottom: 0;
                    }}

                    .file-name {{
                        margin-bottom: 0;
                        flex-basis: 60%;
                    }}

                    .file-actions {{
                        flex-shrink: 0;
                    }}
                }}

                @media (max-width: 480px) {{
                    h1 {{
                        font-size: 1.5rem;
                    }}

                    .action-button {{
                        padding: 10px 16px;
                        font-size: 0.9rem;
                    }}

                    .modal-content {{
                        padding: 20px;
                        margin: 5% auto;
                    }}
                }}
            </style>
            <script>
                // 存储文本内容
                var textContents = {texts_json};

                // 复制文本到剪贴板
                function copyText(index) {{
                    var content = textContents[index];

                    // 创建临时文本区域并复制内容
                    var textArea = document.createElement("textarea");
                    textArea.value = content;
                    document.body.appendChild(textArea);
                    textArea.select();

                    try {{
                        var successful = document.execCommand("copy");
                        if(successful) {{
                            alert("已复制到剪贴板");
                        }} else {{
                            alert("复制失败，请手动复制");
                        }}
                    }} catch (err) {{
                        alert("复制失败，请手动复制: " + err);
                    }}

                    document.body.removeChild(textArea);
                }}

                // 处理文件上传
                function handleFileUpload() {{
                    var form = document.getElementById('fileUploadForm');
                    var formData = new FormData(form);
                    var xhr = new XMLHttpRequest();

                    xhr.open('POST', '/upload/file', true);
                    xhr.onload = function() {{
                        if (xhr.status === 200) {{
                            alert('文件上传成功！');
                            closeModal('fileUploadModal');
                            location.reload();
                        }} else {{
                            alert('文件上传失败: ' + xhr.responseText);
                        }}
                    }};
                    xhr.send(formData);
                    return false;
                }}

                // 处理文本上传（使用JSON格式）
                function handleTextUpload() {{
                    var form = document.getElementById('textUploadForm');
                    var textarea = form.querySelector('textarea[name="text"]');
                    var textContent = textarea.value;

                    if (!textContent) {{
                        alert('请输入文本内容');
                        return false;
                    }}

                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/upload/text', true);
                    xhr.setRequestHeader('Content-Type', 'application/json; charset=utf-8');

                    xhr.onload = function() {{
                        if (xhr.status === 200) {{
                            alert('文本上传成功！');
                            closeModal('textUploadModal');
                            location.reload();
                        }} else {{
                            alert('文本上传失败: ' + xhr.responseText);
                        }}
                    }};

                    var data = JSON.stringify({{ text: textContent }});
                    xhr.send(data);
                    return false;
                }}

                // 打开模态框
                function openModal(modalId) {{
                    document.getElementById(modalId).style.display = 'block';
                }}

                // 关闭模态框
                function closeModal(modalId) {{
                    document.getElementById(modalId).style.display = 'none';
                }}

                // 点击模态框外部关闭
                window.onclick = function(event) {{
                    if (event.target.className === 'modal') {{
                        event.target.style.display = 'none';
                    }}
                }}
            </script>
        </head>
        <body>
            <div class="container">
                <h1>📁 灵卡面板·局域网文件共享</h1>

                <div class="upload-buttons">
                    <button class="action-button" onclick="openModal('fileUploadModal')">上传文件</button>
                    <button class="action-button" onclick="openModal('textUploadModal')">上传文本</button>
                </div>

                <div class="file-list">
        """

        # 添加文件列表
        for item in self.server.file_data["files"]:
            uploader = item.get("uploader", "未知")
            if item["type"] == "file":
                html += f'''
                <div class="file-item">
                    <div style="flex-grow: 1;">
                        <div class="file-name">📄 {item["name"]}</div>
                        <div class="file-info">上传者: {uploader}</div>
                    </div>
                    <div class="file-actions">
                        <a href="/file/{item["name"]}" download>
                            <button class="action-button">下载</button>
                        </a>
                    </div>
                </div>
                '''
            elif item["type"] == "folder":
                html += f'''
                <div class="file-item">
                    <div style="flex-grow: 1;">
                        <a class="file-name folder" href="/file/{item["name"]}">📁 {item["name"]}</a>
                        <div class="file-info">上传者: {uploader}</div>
                    </div>
                </div>
                '''

        # 添加文本内容列表
        for i, item in enumerate(self.server.file_data["texts"]):
            uploader = item.get("uploader", "未知")
            # 显示文本的前30个字符
            display_text = item["content"][:30] + "..." if len(item["content"]) > 30 else item["content"]
            html += f'''
            <div class="file-item">
                <div style="flex-grow: 1;">
                    <div class="file-name">📝 {display_text}</div>
                    <div class="file-info">上传者: {uploader}</div>
                </div>
                <div class="file-actions">
                    <button class="action-button" onclick="copyText({i})">复制</button>
                </div>
            </div>
            '''

        # 添加文件上传模态框
        html += """
                </div>

                <!-- 文件上传模态框 -->
                <div id="fileUploadModal" class="modal">
                    <div class="modal-content">
                        <span class="close" onclick="closeModal('fileUploadModal')">&times;</span>
                        <h2>上传文件</h2>
                        <form id="fileUploadForm" class="upload-form" onsubmit="return handleFileUpload()">
                            <input type="file" name="file" required>
                            <br><br>
                            <input type="submit" value="上传文件">
                        </form>
                    </div>
                </div>

                <!-- 文本上传模态框 -->
                <div id="textUploadModal" class="modal">
                    <div class="modal-content">
                        <span class="close" onclick="closeModal('textUploadModal')">&times;</span>
                        <h2>上传文本</h2>
                        <form id="textUploadForm" class="upload-form" onsubmit="return handleTextUpload()">
                            <textarea name="text" rows="4" placeholder="输入文本内容..." required></textarea>
                            <br>
                            <input type="submit" value="上传文本">
                        </form>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return html

    def generate_directory_listing(self, dir_path, web_path):
        """生成目录列表HTML页面"""
        # 获取目录名
        dir_name = os.path.basename(dir_path)

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>目录: {dir_name}</title>
            <style>
                :root {{
                    --primary-color: #007aff;
                    --primary-hover: #0056b3;
                    --background: #f5f5f7;
                    --card-bg: white;
                    --text-color: #333;
                    --text-secondary: #666;
                    --border-color: #eee;
                    --shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}

                * {{
                    box-sizing: border-box;
                }}

                body {{ 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
                    margin: 0; 
                    padding: 20px; 
                    background-color: var(--background); 
                    color: var(--text-color);
                    font-size: 16px;
                    line-height: 1.5;
                }}

                h1 {{ 
                    color: var(--text-color); 
                    margin-top: 0;
                    font-size: 1.8rem;
                }}

                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                }}

                .back-link {{
                    margin-bottom: 20px; 
                    display: inline-block; 
                    color: var(--primary-color);
                    text-decoration: none;
                    font-size: 1rem;
                    min-height: 44px;
                    display: inline-flex;
                    align-items: center;
                }}

                .back-link:hover {{
                    text-decoration: underline;
                }}

                .file-list {{ 
                    background: var(--card-bg); 
                    border-radius: 12px; 
                    padding: 0; 
                    box-shadow: var(--shadow); 
                    overflow: hidden;
                }}

                .file-item {{ 
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 16px; 
                    border-bottom: 1px solid var(--border-color); 
                }}

                .file-item:last-child {{ 
                    border-bottom: none; 
                }}

                .file-name {{ 
                    flex-grow: 1;
                    color: var(--primary-color); 
                    text-decoration: none; 
                    cursor: default;
                }}

                .file-name.folder {{ 
                    font-weight: bold; 
                    cursor: pointer; 
                }}

                .file-name.folder:hover {{ 
                    text-decoration: underline; 
                }}

                .action-button {{ 
                    background-color: var(--primary-color);
                    color: white;
                    border: none;
                    padding: 10px 16px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 0.9rem;
                    min-height: 44px;
                    min-width: 44px;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                }}

                .action-button:hover {{ 
                    background-color: var(--primary-hover); 
                }}

                /* 响应式设计 */
                @media (max-width: 480px) {{
                    h1 {{
                        font-size: 1.5rem;
                    }}

                    .action-button {{
                        padding: 8px 12px;
                        font-size: 0.8rem;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <a class="back-link" href="/">← 返回文件列表</a>
                <h1>📁 目录: {dir_name}</h1>
                <div class="file-list">
        """

        # 添加父目录链接（如果不是根目录）
        if web_path != '/file/':
            # 获取父目录路径
            parent_path = os.path.dirname(web_path.rstrip('/'))
            if parent_path == '/file':
                parent_path = '/'
            html += f'''
            <div class="file-item">
                <a class="file-name folder" href="{parent_path}">📁 ../</a>
                <span></span> <!-- 占位符，保持布局一致 -->
            </div>
            '''

        # 添加目录内容
        try:
            for item in sorted(os.listdir(dir_path)):
                item_path = os.path.join(dir_path, item)

                # 构建web路径，确保以/file/开头
                # 从web_path中提取相对路径部分（去掉/file/前缀）
                relative_path = web_path[6:]  # 去掉前面的'/file/'
                if relative_path:
                    # 如果当前已经在子目录中，需要将子目录路径与文件名组合
                    web_item_path = f"/file/{os.path.join(relative_path, item)}"
                else:
                    # 如果在根目录，直接使用文件名
                    web_item_path = f"/file/{item}"

                if os.path.isdir(item_path):
                    html += f'''
                    <div class="file-item">
                        <a class="file-name folder" href="{web_item_path}">📁 {item}/</a>
                        <span></span> <!-- 占位符，保持布局一致 -->
                    </div>
                    '''
                else:
                    html += f'''
                    <div class="file-item">
                        <span class="file-name">📄 {item}</span>
                        <a href="{web_item_path}" download>
                            <button class="action-button">下载</button>
                        </a>
                    </div>
                    '''
        except PermissionError:
            html += '<div class="file-item">无权限访问此目录</div>'

        html += """
                </div>
            </div>
        </body>
        </html>
        """
        return html

    def log_message(self, format, *args):
        # 禁用默认的日志输出
        pass