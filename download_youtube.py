#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube视频下载脚本
使用yt-dlp下载YouTube视频到本地
"""

import os
import sys
import argparse
from pathlib import Path
import yt_dlp

# 设置Windows控制台编码为UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass


def download_video(url, output_dir="downloads", quality="best"):
    """
    下载YouTube视频
    
    Args:
        url: YouTube视频链接
        output_dir: 输出目录，默认为"downloads"
        quality: 视频质量，可选值: "best", "worst", "720p", "1080p"等
    """
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # 检查是否有ffmpeg用于合并
    import shutil
    has_ffmpeg = shutil.which('ffmpeg')
    
    # 配置yt-dlp选项
    # Plan B: 使用更严格的格式选择策略，完全避免MPEG-TS格式
    # 明确排除HLS流（m3u8）和MPEG-TS格式，只选择兼容的格式
    ydl_opts = {
        'outtmpl': str(output_path / '%(title)s.%(ext)s'),
        'noplaylist': True,  # 只下载单个视频，不下载播放列表
        'prefer_free_formats': False,  # 不优先选择免费格式
        'no_warnings': False,
        # 关键：明确排除HLS流格式（通常会导致MPEG-TS问题）
        'format_sort': ['ext:mp4', 'ext:webm', 'res', 'codec:h264', 'codec:vp9'],
    }
    
    # 根据是否有ffmpeg和quality参数调整格式选择
    # 完全避免HLS流和MPEG-TS格式
    if has_ffmpeg:
        # 有ffmpeg时，可以使用分离的视频+音频格式，合并为mp4
        ydl_opts['merge_output_format'] = 'mp4'
        if quality == "best":
            # 明确排除HLS格式（format_id 96等），只选择mp4/webm
            ydl_opts['format'] = 'bestvideo[ext=mp4][protocol!=m3u8]+bestaudio[ext=m4a][protocol!=m3u8]/bestvideo[ext=webm][protocol!=m3u8]+bestaudio[ext=webm][protocol!=m3u8]/best[ext=mp4][protocol!=m3u8]/best[ext=webm][protocol!=m3u8]/best[protocol!=m3u8]'
        elif quality == "720p":
            ydl_opts['format'] = 'bestvideo[height<=720][ext=mp4][protocol!=m3u8]+bestaudio[ext=m4a][protocol!=m3u8]/bestvideo[height<=720][ext=webm][protocol!=m3u8]+bestaudio[ext=webm][protocol!=m3u8]/best[height<=720][ext=mp4][protocol!=m3u8]/best[height<=720][protocol!=m3u8]'
        elif quality == "1080p":
            ydl_opts['format'] = 'bestvideo[height<=1080][ext=mp4][protocol!=m3u8]+bestaudio[ext=m4a][protocol!=m3u8]/bestvideo[height<=1080][ext=webm][protocol!=m3u8]+bestaudio[ext=webm][protocol!=m3u8]/best[height<=1080][ext=mp4][protocol!=m3u8]/best[height<=1080][protocol!=m3u8]'
        elif quality == "worst":
            ydl_opts['format'] = 'worst[ext=mp4][protocol!=m3u8]/worst[ext=webm][protocol!=m3u8]/worst[protocol!=m3u8]'
    else:
        # 没有ffmpeg时，只选择单一格式（不需要合并的）
        # 完全排除HLS流，只选择mp4/webm格式
        if quality == "best":
            # 关键：排除m3u8协议（HLS流），避免MPEG-TS问题
            ydl_opts['format'] = 'best[ext=mp4][protocol!=m3u8]/best[ext=webm][protocol!=m3u8]/best[protocol!=m3u8][vcodec!=none][acodec!=none]'
        elif quality == "720p":
            ydl_opts['format'] = 'best[height<=720][ext=mp4][protocol!=m3u8]/best[height<=720][ext=webm][protocol!=m3u8]/best[height<=720][protocol!=m3u8][vcodec!=none][acodec!=none]'
        elif quality == "1080p":
            ydl_opts['format'] = 'best[height<=1080][ext=mp4][protocol!=m3u8]/best[height<=1080][ext=webm][protocol!=m3u8]/best[height<=1080][protocol!=m3u8][vcodec!=none][acodec!=none]'
        elif quality == "worst":
            ydl_opts['format'] = 'worst[ext=mp4][protocol!=m3u8]/worst[ext=webm][protocol!=m3u8]/worst[protocol!=m3u8][vcodec!=none][acodec!=none]'
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 获取视频信息
            print(f"正在获取视频信息: {url}")
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            print(f"视频标题: {title}")
            print(f"时长: {duration // 60}分{duration % 60}秒")
            print(f"开始下载...")
            
            # 下载视频
            ydl.download([url])
            
            print(f"\n[成功] 下载完成！")
            print(f"保存位置: {output_path.absolute()}")
            
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        print(f"[错误] 下载失败: {error_msg}")
        if "ffmpeg" in error_msg.lower():
            print("\n提示: 如果需要下载最佳质量的视频，请安装ffmpeg:")
            print("  Windows: 下载 https://ffmpeg.org/download.html 并添加到PATH")
            print("  或使用: winget install ffmpeg")
        sys.exit(1)
    except Exception as e:
        print(f"[错误] 发生错误: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='下载YouTube视频到本地',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python download_youtube.py https://www.youtube.com/watch?v=VIDEO_ID
  python download_youtube.py https://www.youtube.com/watch?v=VIDEO_ID --output my_videos
  python download_youtube.py https://www.youtube.com/watch?v=VIDEO_ID --quality 720p
        """
    )
    
    parser.add_argument('url', help='YouTube视频链接')
    parser.add_argument(
        '-o', '--output',
        default='downloads',
        help='输出目录 (默认: downloads)'
    )
    parser.add_argument(
        '-q', '--quality',
        choices=['best', 'worst', '720p', '1080p'],
        default='best',
        help='视频质量 (默认: best)'
    )
    
    args = parser.parse_args()
    
    download_video(args.url, args.output, args.quality)


if __name__ == "__main__":
    main()

