#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube视频下载Web应用
提供网页界面下载YouTube视频
"""

import os
import sys
import json
import threading
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import yt_dlp
from datetime import datetime

# 设置Windows控制台编码为UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

app = Flask(__name__)
CORS(app)

# 配置
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

# 存储下载任务状态
download_tasks = {}


def get_video_info(url):
    """获取视频信息（不下载）"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', ''),
                'uploader': info.get('uploader', 'Unknown'),
                'view_count': info.get('view_count', 0),
                'success': True
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def download_video_task(task_id, url, quality="best", download_dir=None):
    """后台下载任务"""
    # 使用自定义目录或默认目录
    if download_dir:
        output_path = Path(download_dir)
    else:
        output_path = DOWNLOAD_DIR
    output_path.mkdir(parents=True, exist_ok=True)
    has_ffmpeg = False
    try:
        import shutil
        has_ffmpeg = shutil.which('ffmpeg') is not None
    except:
        pass
    
    ydl_opts = {
        'outtmpl': str(output_path / '%(title)s.%(ext)s'),
        'noplaylist': True,
        'prefer_free_formats': False,
        'format_sort': ['ext:mp4', 'ext:webm', 'res', 'codec:h264', 'codec:vp9'],
        'progress_hooks': [lambda d: update_progress(task_id, d)],
    }
    
    # 格式选择策略（避免MPEG-TS问题）
    if has_ffmpeg:
        ydl_opts['merge_output_format'] = 'mp4'
        if quality == "best":
            ydl_opts['format'] = 'bestvideo[ext=mp4][protocol!=m3u8]+bestaudio[ext=m4a]/bestvideo[ext=webm][protocol!=m3u8]+bestaudio[ext=webm]/best[ext=mp4][protocol!=m3u8]/best[ext=webm][protocol!=m3u8]/best[protocol!=m3u8]'
        elif quality == "720p":
            ydl_opts['format'] = 'bestvideo[height<=720][ext=mp4][protocol!=m3u8]+bestaudio[ext=m4a]/bestvideo[height<=720][ext=webm][protocol!=m3u8]+bestaudio[ext=webm]/best[height<=720][ext=mp4][protocol!=m3u8]/best[height<=720][protocol!=m3u8]'
        elif quality == "1080p":
            ydl_opts['format'] = 'bestvideo[height<=1080][ext=mp4][protocol!=m3u8]+bestaudio[ext=m4a]/bestvideo[height<=1080][ext=webm][protocol!=m3u8]+bestaudio[ext=webm]/best[height<=1080][ext=mp4][protocol!=m3u8]/best[height<=1080][protocol!=m3u8]'
        elif quality == "worst":
            ydl_opts['format'] = 'worst[ext=mp4][protocol!=m3u8]/worst[ext=webm][protocol!=m3u8]/worst[protocol!=m3u8]'
    else:
        if quality == "best":
            ydl_opts['format'] = 'best[ext=mp4][protocol!=m3u8][vcodec!=none][acodec!=none]/best[ext=webm][protocol!=m3u8][vcodec!=none][acodec!=none]/best[protocol!=m3u8][vcodec!=none][acodec!=none]'
        elif quality == "720p":
            ydl_opts['format'] = 'best[height<=720][ext=mp4][protocol!=m3u8][vcodec!=none][acodec!=none]/best[height<=720][ext=webm][protocol!=m3u8][vcodec!=none][acodec!=none]/best[height<=720][protocol!=m3u8][vcodec!=none][acodec!=none]'
        elif quality == "1080p":
            ydl_opts['format'] = 'best[height<=1080][ext=mp4][protocol!=m3u8][vcodec!=none][acodec!=none]/best[height<=1080][ext=webm][protocol!=m3u8][vcodec!=none][acodec!=none]/best[height<=1080][protocol!=m3u8][vcodec!=none][acodec!=none]'
        elif quality == "worst":
            ydl_opts['format'] = 'worst[ext=mp4][protocol!=m3u8][vcodec!=none][acodec!=none]/worst[ext=webm][protocol!=m3u8][vcodec!=none][acodec!=none]/worst[protocol!=m3u8][vcodec!=none][acodec!=none]'
    
    try:
        download_tasks[task_id]['status'] = 'downloading'
        download_tasks[task_id]['progress'] = 0
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # 获取实际下载的文件名
            actual_file = Path(filename)
            if not actual_file.exists():
                # 尝试查找文件
                for ext in ['.mp4', '.webm', '.mkv']:
                    test_file = actual_file.with_suffix(ext)
                    if test_file.exists():
                        actual_file = test_file
                        break
            
            download_tasks[task_id]['status'] = 'completed'
            download_tasks[task_id]['progress'] = 100
            download_tasks[task_id]['filename'] = actual_file.name
            download_tasks[task_id]['filepath'] = str(actual_file)
            download_tasks[task_id]['download_dir'] = str(output_path)
            
    except Exception as e:
        download_tasks[task_id]['status'] = 'error'
        download_tasks[task_id]['error'] = str(e)


def update_progress(task_id, d):
    """更新下载进度"""
    if task_id in download_tasks:
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            if total > 0:
                progress = int((downloaded / total) * 100)
                download_tasks[task_id]['progress'] = progress
                download_tasks[task_id]['speed'] = d.get('speed', 0)
                download_tasks[task_id]['eta'] = d.get('eta', 0)


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/info', methods=['POST'])
def get_info():
    """获取视频信息"""
    data = request.json
    url = data.get('url', '')
    
    if not url:
        return jsonify({'success': False, 'error': 'URL不能为空'})
    
    info = get_video_info(url)
    return jsonify(info)


@app.route('/api/download', methods=['POST'])
def start_download():
    """开始下载视频"""
    data = request.json
    url = data.get('url', '')
    quality = data.get('quality', 'best')
    download_dir = data.get('download_dir', '').strip()
    
    if not url:
        return jsonify({'success': False, 'error': 'URL不能为空'})
    
    # 验证下载目录
    if download_dir:
        try:
            download_path = Path(download_dir)
            # 检查是否为有效路径
            if not download_path.is_absolute() and not download_path.exists():
                # 相对路径，检查父目录是否存在
                parent = download_path.parent
                if parent and not parent.exists():
                    return jsonify({'success': False, 'error': f'下载目录无效: {download_dir}'})
        except Exception as e:
            return jsonify({'success': False, 'error': f'下载目录错误: {str(e)}'})
    
    # 生成任务ID
    task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    # 初始化任务状态
    download_tasks[task_id] = {
        'task_id': task_id,
        'url': url,
        'quality': quality,
        'download_dir': download_dir if download_dir else str(DOWNLOAD_DIR),
        'status': 'pending',
        'progress': 0,
        'filename': None,
        'filepath': None,
        'error': None
    }
    
    # 在后台线程中开始下载
    thread = threading.Thread(target=download_video_task, args=(task_id, url, quality, download_dir if download_dir else None))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'task_id': task_id
    })


@app.route('/api/status/<task_id>')
def get_status(task_id):
    """获取下载状态"""
    if task_id not in download_tasks:
        return jsonify({'success': False, 'error': '任务不存在'})
    
    task = download_tasks[task_id]
    return jsonify({
        'success': True,
        'task': {
            'task_id': task['task_id'],
            'status': task['status'],
            'progress': task.get('progress', 0),
            'filename': task.get('filename'),
            'error': task.get('error'),
            'speed': task.get('speed', 0),
            'eta': task.get('eta', 0)
        }
    })


@app.route('/api/downloads')
def list_downloads():
    """列出所有已下载的文件"""
    # 获取查询参数中的目录（可选）
    download_dir = request.args.get('dir', '').strip()
    
    # 确定要扫描的目录列表
    dirs_to_scan = []
    if download_dir:
        try:
            dirs_to_scan.append(Path(download_dir))
        except:
            pass
    else:
        # 默认目录 + 所有任务中使用的目录
        dirs_to_scan.append(DOWNLOAD_DIR)
        for task in download_tasks.values():
            if task.get('download_dir'):
                try:
                    task_dir = Path(task['download_dir'])
                    if task_dir.exists() and task_dir not in dirs_to_scan:
                        dirs_to_scan.append(task_dir)
                except:
                    pass
    
    files = []
    scanned_dirs = set()
    
    for scan_dir in dirs_to_scan:
        if not scan_dir.exists():
            continue
        
        # 避免重复扫描
        scan_dir_str = str(scan_dir.resolve())
        if scan_dir_str in scanned_dirs:
            continue
        scanned_dirs.add(scan_dir_str)
        
        for file_path in scan_dir.glob('*'):
            if file_path.is_file() and file_path.suffix in ['.mp4', '.webm', '.mkv']:
                stat = file_path.stat()
                files.append({
                    'name': file_path.name,
                    'path': str(file_path),
                    'dir': str(scan_dir),
                    'size': stat.st_size,
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
    
    # 按修改时间排序（最新的在前）
    files.sort(key=lambda x: x['modified'], reverse=True)
    
    return jsonify({
        'success': True,
        'files': files
    })


@app.route('/api/download/<filename>')
def download_file(filename):
    """下载文件"""
    # 获取查询参数中的目录（可选）
    download_dir = request.args.get('dir', '').strip()
    
    # 确定文件路径
    if download_dir:
        try:
            file_path = Path(download_dir) / filename
        except:
            file_path = DOWNLOAD_DIR / filename
    else:
        # 尝试在默认目录和所有任务目录中查找
        file_path = None
        search_dirs = [DOWNLOAD_DIR]
        
        # 添加所有任务中使用的目录
        for task in download_tasks.values():
            if task.get('download_dir'):
                try:
                    task_dir = Path(task['download_dir'])
                    if task_dir.exists() and task_dir not in search_dirs:
                        search_dirs.append(task_dir)
                except:
                    pass
        
        # 在所有目录中搜索文件
        for search_dir in search_dirs:
            test_path = search_dir / filename
            if test_path.exists():
                file_path = test_path
                break
        
        if not file_path:
            file_path = DOWNLOAD_DIR / filename
    
    if not file_path.exists():
        return jsonify({'success': False, 'error': '文件不存在'}), 404
    
    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename
    )


@app.route('/api/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    """删除文件"""
    # 获取查询参数中的目录（可选）
    download_dir = request.args.get('dir', '').strip()
    
    # 确定文件路径
    if download_dir:
        try:
            file_path = Path(download_dir) / filename
        except:
            file_path = DOWNLOAD_DIR / filename
    else:
        # 尝试在默认目录和所有任务目录中查找
        file_path = None
        search_dirs = [DOWNLOAD_DIR]
        
        # 添加所有任务中使用的目录
        for task in download_tasks.values():
            if task.get('download_dir'):
                try:
                    task_dir = Path(task['download_dir'])
                    if task_dir.exists() and task_dir not in search_dirs:
                        search_dirs.append(task_dir)
                except:
                    pass
        
        # 在所有目录中搜索文件
        for search_dir in search_dirs:
            test_path = search_dir / filename
            if test_path.exists():
                file_path = test_path
                break
        
        if not file_path:
            file_path = DOWNLOAD_DIR / filename
    
    if not file_path.exists():
        return jsonify({'success': False, 'error': '文件不存在'}), 404
    
    try:
        file_path.unlink()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("YouTube视频下载Web应用 - 本地版本")
    print("=" * 60)
    print(f"访问地址: http://localhost:5000")
    print(f"下载目录: {DOWNLOAD_DIR.absolute()}")
    print("=" * 60)
    print("提示: 按 Ctrl+C 停止服务器")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=5000)

