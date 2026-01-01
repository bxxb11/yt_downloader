#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复已下载的视频文件
将MPEG-TS格式或其他格式转换为可播放的MP4格式
需要ffmpeg支持
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# 设置Windows控制台编码为UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass


def check_ffmpeg():
    """检查ffmpeg是否可用"""
    if shutil.which('ffmpeg'):
        try:
            subprocess.run(['ffmpeg', '-version'], 
                          capture_output=True, 
                          check=True)
            return True
        except:
            return False
    return False


def fix_video(input_file, output_file=None, keep_original=True):
    """
    修复视频文件，重新编码为标准的MP4格式
    
    Args:
        input_file: 输入视频文件路径
        output_file: 输出文件路径（如果为None，则自动生成）
        keep_original: 是否保留原文件
    """
    if not os.path.exists(input_file):
        print(f"[错误] 文件不存在: {input_file}")
        return False
    
    if output_file is None:
        # 创建修复后的文件名
        path = Path(input_file)
        output_file = str(path.parent / f"{path.stem}_fixed.mp4")
    
    print(f"正在修复: {os.path.basename(input_file)}")
    print(f"输出文件: {os.path.basename(output_file)}")
    
    # 使用ffmpeg重新编码视频为标准MP4格式
    # 使用copy编码器尝试快速修复，如果不行则重新编码
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-c:v', 'libx264',  # 使用H.264视频编码
        '-c:a', 'aac',      # 使用AAC音频编码
        '-movflags', '+faststart',  # 优化web播放，将元数据移到文件开头
        '-preset', 'medium',  # 编码速度和质量平衡
        '-crf', '23',  # 质量设置（18-28，23是默认值）
        '-y',  # 覆盖输出文件
        output_file
    ]
    
    try:
        print("正在重新编码视频...")
        result = subprocess.run(cmd, 
                              capture_output=True, 
                              text=True,
                              check=True)
        print(f"[成功] 修复完成: {output_file}")
        
        # 如果成功且不保留原文件，删除原文件
        if not keep_original and os.path.exists(output_file):
            try:
                os.remove(input_file)
                print(f"[信息] 已删除原文件: {os.path.basename(input_file)}")
            except:
                print(f"[警告] 无法删除原文件: {os.path.basename(input_file)}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"[错误] 修复失败")
        if e.stderr:
            # 只显示关键错误信息
            error_lines = e.stderr.split('\n')
            for line in error_lines[-10:]:  # 显示最后10行
                if line.strip():
                    print(f"  {line}")
        return False
    except FileNotFoundError:
        print("[错误] ffmpeg未找到，请先安装ffmpeg")
        print("  Windows: 下载 https://ffmpeg.org/download.html 并添加到PATH")
        print("  或使用: winget install ffmpeg")
        return False


def fix_all_videos_in_directory(directory="downloads", keep_original=True):
    """修复目录中的所有视频文件"""
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"[错误] 目录不存在: {directory}")
        return
    
    video_extensions = ['.mp4', '.webm', '.mkv', '.flv', '.avi']
    video_files = []
    
    for ext in video_extensions:
        video_files.extend(dir_path.glob(f'*{ext}'))
        video_files.extend(dir_path.glob(f'*{ext.upper()}'))
    
    # 排除已经修复过的文件
    video_files = [f for f in video_files if not f.name.endswith('_fixed.mp4')]
    
    if not video_files:
        print(f"[信息] 在 {directory} 目录中未找到视频文件")
        return
    
    print(f"找到 {len(video_files)} 个视频文件")
    print("-" * 50)
    
    success_count = 0
    for video_file in video_files:
        print(f"\n处理: {video_file.name}")
        if fix_video(str(video_file), keep_original=keep_original):
            success_count += 1
        print("-" * 50)
    
    print(f"\n[完成] 成功修复 {success_count}/{len(video_files)} 个文件")


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='修复已下载的视频文件（修复MPEG-TS等问题）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python fix_videos.py                    # 修复downloads目录中的所有视频
  python fix_videos.py video.mp4          # 修复指定视频文件
  python fix_videos.py --directory my_videos  # 修复指定目录中的视频
  python fix_videos.py --replace           # 修复后替换原文件
        """
    )
    
    parser.add_argument(
        'file',
        nargs='?',
        help='要修复的视频文件路径（如果未指定，则修复目录中的所有视频）'
    )
    parser.add_argument(
        '-d', '--directory',
        default='downloads',
        help='要处理的目录（默认: downloads）'
    )
    parser.add_argument(
        '--replace',
        action='store_true',
        help='修复后替换原文件（默认保留原文件）'
    )
    
    args = parser.parse_args()
    
    if not check_ffmpeg():
        print("[错误] 需要ffmpeg来修复视频文件")
        print("\n请安装ffmpeg:")
        print("  Windows: 下载 https://ffmpeg.org/download.html 并添加到PATH")
        print("  或使用: winget install ffmpeg")
        sys.exit(1)
    
    if args.file:
        # 修复单个文件
        fix_video(args.file, keep_original=not args.replace)
    else:
        # 修复目录中的所有视频
        fix_all_videos_in_directory(args.directory, keep_original=not args.replace)


if __name__ == "__main__":
    main()
