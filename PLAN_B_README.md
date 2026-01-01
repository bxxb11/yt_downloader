# Plan B: 无需ffmpeg的视频修复方案

由于网络问题无法安装ffmpeg时，可以使用以下Plan B方案：

## 方案1: 重新下载（推荐）

使用 `redownload_fixed.py` 脚本重新下载视频，使用更严格的格式过滤：

```bash
python redownload_fixed.py "视频链接"
```

**特点**：
- 完全排除HLS流（m3u8协议）
- 明确排除format_id 96（导致MPEG-TS问题的格式）
- 只选择兼容的mp4/webm格式
- 下载的文件会添加 `_fixed` 后缀

## 方案2: 使用VLC播放器

如果重新下载后仍有问题，可以使用VLC播放器打开视频：

1. 下载VLC: https://www.videolan.org/vlc/
2. 用VLC打开无法播放的视频文件
3. VLC通常能处理MPEG-TS格式的视频

## 方案3: 修改下载脚本

已更新的 `download_youtube.py` 现在默认使用更严格的格式过滤，新下载的视频应该更少出现MPEG-TS问题。

## 注意事项

- 某些YouTube视频可能只提供HLS流格式，这种情况下Plan B可能无法完全避免MPEG-TS问题
- 如果Plan B仍然失败，建议：
  1. 等待网络恢复后安装ffmpeg
  2. 或使用VLC播放器播放视频
  3. 或尝试下载其他质量的视频（720p/1080p）

## 使用示例

```bash
# 重新下载有问题的视频
python redownload_fixed.py "https://youtu.be/VIDEO_ID"

# 指定质量重新下载
python redownload_fixed.py "https://youtu.be/VIDEO_ID" --quality 720p
```

