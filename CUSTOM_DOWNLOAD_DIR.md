# 自定义下载目录功能

## ✨ 新功能

现在您可以自定义视频下载的保存位置了！

## 🎯 使用方法

### 在网页界面中

1. **打开下载页面**
   - 启动服务器: `python app.py`
   - 访问: http://localhost:5000

2. **输入视频链接和选择质量**
   - 粘贴YouTube视频链接
   - 选择视频质量

3. **设置下载目录（可选）**
   - 在"下载目录"输入框中输入您想要的路径
   - **Windows示例**: `D:\Videos` 或 `C:\Users\YourName\Downloads\YouTube`
   - **macOS/Linux示例**: `/home/user/videos` 或 `~/Downloads/YouTube`
   - **留空**: 将使用默认的 `downloads/` 目录

4. **开始下载**
   - 点击"获取视频信息"
   - 点击"开始下载"

## 📁 目录格式

### Windows
```
D:\Videos
C:\Users\YourName\Downloads\YouTube
E:\MyVideos\YouTube
```

### macOS/Linux
```
/home/user/videos
~/Downloads/YouTube
/Users/YourName/Movies
```

## ⚠️ 注意事项

1. **路径有效性**
   - 确保输入的路径是有效的
   - 如果目录不存在，系统会自动创建（如果父目录存在）
   - 相对路径会相对于项目根目录

2. **权限**
   - 确保您有写入权限到指定目录
   - 如果权限不足，下载会失败

3. **路径格式**
   - Windows: 使用反斜杠 `\` 或正斜杠 `/` 都可以
   - macOS/Linux: 使用正斜杠 `/`
   - 路径末尾的斜杠会被自动处理

4. **默认行为**
   - 如果留空，使用默认的 `downloads/` 目录
   - 默认目录在项目根目录下

## 🔍 文件管理

### 查看文件列表

- 文件列表会显示所有已下载的文件
- 如果文件来自自定义目录，会显示目录路径
- 可以下载或删除来自任何目录的文件

### 文件操作

- **下载**: 点击"下载"按钮，文件会从正确的目录下载
- **删除**: 点击"删除"按钮，文件会从正确的目录删除

## 💡 使用示例

### 示例1: 下载到D盘Videos文件夹
```
下载目录: D:\Videos
```

### 示例2: 下载到用户Downloads文件夹
```
Windows: C:\Users\YourName\Downloads\YouTube
macOS: ~/Downloads/YouTube
Linux: /home/user/Downloads/YouTube
```

### 示例3: 使用默认目录
```
下载目录: (留空)
→ 文件会下载到项目目录下的 downloads/ 文件夹
```

## 🛠️ 技术细节

### 后端实现

- `download_video_task()` 函数接受 `download_dir` 参数
- 如果提供了自定义目录，会创建并使用该目录
- 任务状态中会保存下载目录信息

### 前端实现

- 添加了"下载目录"输入框
- 下载时会发送 `download_dir` 参数
- 文件列表会显示文件所在目录

### API变更

- `POST /api/download`: 接受 `download_dir` 参数
- `GET /api/downloads`: 支持 `?dir=` 查询参数（可选）
- `GET /api/download/<filename>`: 支持 `?dir=` 查询参数
- `DELETE /api/delete/<filename>`: 支持 `?dir=` 查询参数

## 🎉 优势

1. **灵活性**: 可以下载到任何您想要的位置
2. **组织性**: 可以按项目、日期等组织文件
3. **兼容性**: 完全向后兼容，留空使用默认目录
4. **智能搜索**: 文件列表会自动搜索所有使用过的目录

---

**享受更灵活的视频下载体验！** 🎬

