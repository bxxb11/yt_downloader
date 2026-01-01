#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plan B: 重新下载视频（使用更严格的格式过滤，避免MPEG-TS问题）
如果视频无法播放，使用此脚本重新下载
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


def redownload_video(url, output_dir="downloads", quality="best"):
    """
    重新下载视频，使用更严格的格式过滤，完全避免MPEG-TS格式
    
    Args:
        url: YouTube视频链接
        output_dir: 输出目录，默认为"downloads"
        quality: 视频质量，可选值: "best", "worst", "720p", "1080p"等
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Plan B: 使用最严格的格式过滤，完全避免MPEG-TS和HLS流
    ydl_opts = {
        'outtmpl': str(output_path / '%(title)s_fixed.%(ext)s'),
        'noplaylist': True,
        'prefer_free_formats': False,
        # 关键：完全排除HLS流（m3u8），这是导致MPEG-TS问题的主要原因
        'format_sort': ['ext:mp4', 'ext:webm', 'res', 'codec:h264', 'codec:vp9'],
    }
    
    # 只选择单一格式（不需要合并），完全排除HLS流
    # 明确排除format_id 96（HLS流格式，会导致MPEG-TS问题）
    if quality == "best":
        # 排除m3u8协议和format_id 96，只选择mp4/webm格式，确保有视频和音频
        ydl_opts['format'] = 'best[ext=mp4][protocol!=m3u8][format_id!=96][vcodec!=none][acodec!=none]/best[ext=webm][protocol!=m3u8][format_id!=96][vcodec!=none][acodec!=none]/best[protocol!=m3u8][format_id!=96][vcodec!=none][acodec!=none]'
    elif quality == "720p":
        ydl_opts['format'] = 'best[height<=720][ext=mp4][protocol!=m3u8][format_id!=96][vcodec!=none][acodec!=none]/best[height<=720][ext=webm][protocol!=m3u8][format_id!=96][vcodec!=none][acodec!=none]/best[height<=720][protocol!=m3u8][format_id!=96][vcodec!=none][acodec!=none]'
    elif quality == "1080p":
        ydl_opts['format'] = 'best[height<=1080][ext=mp4][protocol!=m3u8][format_id!=96][vcodec!=none][acodec!=none]/best[height<=1080][ext=webm][protocol!=m3u8][format_id!=96][vcodec!=none][acodec!=none]/best[height<=1080][protocol!=m3u8][format_id!=96][vcodec!=none][acodec!=none]'
    elif quality == "worst":
        ydl_opts['format'] = 'worst[ext=mp4][protocol!=m3u8][format_id!=96][vcodec!=none][acodec!=none]/worst[ext=webm][protocol!=m3u8][format_id!=96][vcodec!=none][acodec!=none]/worst[protocol!=m3u8][format_id!=96][vcodec!=none][acodec!=none]'
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"正在重新下载（使用Plan B格式过滤）: {url}")
            print("策略: 完全排除HLS流，只选择兼容的mp4/webm格式")
            
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            print(f"视频标题: {title}")
            print(f"时长: {duration // 60}分{duration % 60}秒")
            print(f"开始下载...")
            
            ydl.download([url])
            
            print(f"\n[成功] 重新下载完成！")
            print(f"保存位置: {output_path.absolute()}")
            print(f"文件名包含 '_fixed' 后缀，表示使用Plan B策略下载")
            
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        print(f"[错误] 重新下载失败: {error_msg}")
        print("\n提示: 如果仍然失败，可能需要安装ffmpeg来合并视频和音频")
        sys.exit(1)
    except Exception as e:
        print(f"[错误] 发生错误: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Plan B: 重新下载视频（避免MPEG-TS格式问题）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Plan B策略:
  - 完全排除HLS流（m3u8协议），这是导致MPEG-TS问题的主要原因
  - 只选择兼容的mp4/webm格式
  - 确保视频和音频都存在

示例:
  python redownload_fixed.py https://www.youtube.com/watch?v=VIDEO_ID
  python redownload_fixed.py https://www.youtube.com/watch?v=VIDEO_ID --quality 720p
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
    
    redownload_video(args.url, args.output, args.quality)


if __name__ == "__main__":
    main()

