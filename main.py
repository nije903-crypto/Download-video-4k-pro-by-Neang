#!/usr/bin/env python3
"""
📱 VIDEO DOWNLOADER PRO - Mobile Optimized
Facebook • TikTok • Pinterest
"""

import os
import re
import time
import shutil
import subprocess
import sys
import json
import requests
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("\n❌ yt-dlp not installed!")
    print("   Run: pip install yt-dlp\n")
    exit(1)

# ==============================
# CONFIGURATION
# ==============================

STORAGE_HOME = Path.home() / "storage"
GALLERY_FOLDER = STORAGE_HOME / "shared" / "DCIM" / "Camera"
GALLERY_FOLDER.mkdir(parents=True, exist_ok=True)
TEMP_FOLDER = STORAGE_HOME / "downloads"
TEMP_FOLDER.mkdir(parents=True, exist_ok=True)

# ==============================
# STYLE - Mobile Optimized
# ==============================

def print_style(text, color='white', bold=False):
    colors = {
        'red': '\033[91m', 'green': '\033[92m', 'yellow': '\033[93m',
        'blue': '\033[94m', 'magenta': '\033[95m', 'cyan': '\033[96m',
        'white': '\033[97m', 'gray': '\033[90m'
    }
    prefix = '\033[1m' if bold else ''
    prefix += colors.get(color, '')
    print(f"{prefix}{text}\033[0m")

def clear():
    os.system('clear')

def print_header():
    clear()
    print_style("╔══════════════════════════════╗", 'cyan', bold=True)
    print_style("║  🎬  VIDEO DOWNLOADER PRO  ║", 'yellow', bold=True)
    print_style("╠══════════════════════════════╣", 'cyan')
    print_style("║  📱 FB • TT • Pinterest     ║", 'cyan')
    print_style("║  🔄 Multi-API • 4K          ║", 'cyan')
    print_style("╚══════════════════════════════╝", 'cyan', bold=True)
    print()

def print_separator():
    print_style("────────────────────────────", 'gray')

# ==============================
# HELPER FUNCTIONS
# ==============================

def clean_filename(title):
    title = re.sub(r'[<>:"/\\|?*#@&]', '', title)
    title = re.sub(r'[-\s]+', '_', title)
    return title[:50]

def move_to_gallery(filepath):
    try:
        if not filepath or not Path(filepath).exists():
            return None
        filename = Path(filepath).name
        new_path = GALLERY_FOLDER / filename
        if new_path.exists():
            base = new_path.stem
            ext = new_path.suffix
            counter = 1
            while new_path.exists():
                new_path = GALLERY_FOLDER / f"{base}_{counter}{ext}"
                counter += 1
        shutil.move(str(filepath), str(new_path))
        return str(new_path)
    except Exception:
        return None

def merge_audio_video(video_path, audio_path, output_path):
    try:
        print_style("   🎵 Merging audio...", 'gray')
        cmd = [
            'ffmpeg', '-y',
            '-i', str(video_path),
            '-i', str(audio_path),
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-map', '0:v:0',
            '-map', '1:a:0',
            str(output_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and output_path.exists():
            if video_path.exists():
                video_path.unlink()
            if audio_path.exists():
                audio_path.unlink()
            return True
        return False
    except Exception:
        return False

def download_direct_video(video_url, title):
    try:
        clean_title = clean_filename(title)
        filepath = TEMP_FOLDER / f"{clean_title}.mp4"
        
        print_style("   📥 Downloading...", 'blue')
        response = requests.get(video_url, stream=True)
        
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            sys.stdout.write(f"\r   📊 {percent:.1f}%")
                            sys.stdout.flush()
            
            print()
            if filepath.exists() and filepath.stat().st_size > 0:
                print_style("   📁 Moving to Gallery...", 'gray')
                final_path = move_to_gallery(filepath)
                return final_path
        
        return None
    except Exception as e:
        print_style(f"   ⚠️ {str(e)[:30]}", 'yellow')
        return None

# ==============================
# APIs - Facebook (5 APIs)
# ==============================

def extract_facebook_api(url):
    apis = [
        f"https://api.fdownloader.com/api/v1/facebook?url={url}",
        f"https://www.getfvid.com/api/video?url={url}",
        f"https://fbdown.net/api/v1/download?url={url}",
        f"https://snapvid.net/api/v1/facebook?url={url}",
        f"https://fbvideo.net/api/v1/download?url={url}",
    ]
    
    for i, api_url in enumerate(apis, 1):
        try:
            print_style(f"   🔄 FB API {i}...", 'gray')
            response = requests.get(api_url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    video_url = data.get('video_url') or data.get('hd_video_url') or data.get('sd_video_url')
                    title = data.get('title', 'Facebook_Video')
                    if video_url:
                        return {'url': video_url, 'title': title}
                if data.get('video_url'):
                    return {'url': data['video_url'], 'title': data.get('title', 'Facebook_Video')}
                if data.get('hd_video_url'):
                    return {'url': data['hd_video_url'], 'title': data.get('title', 'Facebook_Video')}
        except:
            continue
    return None

# ==============================
# APIs - TikTok (6 APIs)
# ==============================

def extract_tiktok_api(url):
    apis = [
        f"https://www.tikwm.com/api/?url={url}",
        f"https://api.tikmate.cc/api/v1/download?url={url}",
        f"https://tikcdn.com/api/v1/download?url={url}",
        f"https://ssstik.io/api?url={url}",
        f"https://tiksave.com/api/v1/download?url={url}",
        f"https://tiktokdownload.net/api/v1/download?url={url}",
    ]
    
    for i, api_url in enumerate(apis, 1):
        try:
            print_style(f"   🔄 TT API {i}...", 'gray')
            response = requests.get(api_url, timeout=20)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    video_data = data.get('data', {})
                    video_url = video_data.get('play') or video_data.get('wmplay')
                    title = video_data.get('title', 'TikTok_Video')
                    if video_url:
                        return {'url': video_url, 'title': title}
                if data.get('success'):
                    video_url = data.get('video_url')
                    title = data.get('title', 'TikTok_Video')
                    if video_url:
                        return {'url': video_url, 'title': title}
                if data.get('video_url'):
                    return {'url': data['video_url'], 'title': data.get('title', 'TikTok_Video')}
                if data.get('link'):
                    return {'url': data['link'], 'title': data.get('title', 'TikTok_Video')}
        except:
            continue
    return None

# ==============================
# APIs - Pinterest (5 APIs)
# ==============================

def extract_pinterest_api(url):
    apis = [
        f"https://api.pindownloader.com/api/v1/download?url={url}",
        f"https://pinterestdownloader.app/api/v1/download?url={url}",
        f"https://pinterestvid.com/api/v1/video?url={url}",
        f"https://pinvid.com/api/v1/download?url={url}",
        f"https://pinterestdl.com/api/v1/download?url={url}",
    ]
    
    for i, api_url in enumerate(apis, 1):
        try:
            print_style(f"   🔄 Pin API {i}...", 'gray')
            response = requests.get(api_url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get('video_url'):
                    return {'url': data['video_url'], 'title': data.get('title', 'Pinterest_Video')}
                if data.get('hd_video_url'):
                    return {'url': data['hd_video_url'], 'title': data.get('title', 'Pinterest_Video')}
                if data.get('sd_video_url'):
                    return {'url': data['sd_video_url'], 'title': data.get('title', 'Pinterest_Video')}
                if data.get('video'):
                    return {'url': data['video'], 'title': data.get('title', 'Pinterest_Video')}
        except:
            continue
    return None

# ==============================
# GET VIDEO FORMATS
# ==============================

def get_video_formats(url, platform):
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'extract_flat': False,
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                return []
            
            formats = info.get('formats', [])
            video_formats = []
            seen = set()
            
            for f in formats:
                height = f.get('height')
                fps = f.get('fps')
                vcodec = f.get('vcodec')
                format_id = f.get('format_id')
                acodec = f.get('acodec')
                filesize = f.get('filesize')
                
                if height and vcodec != 'none':
                    if height <= 480:
                        label = f"SD {height}p"
                        icon = "🔵"
                    elif height <= 720:
                        label = f"HD {height}p"
                        icon = "🟢"
                    elif height <= 1080:
                        label = f"FHD {height}p"
                        icon = "🟡"
                    elif height <= 2160:
                        label = f"4K {height}p"
                        icon = "⭐"
                    else:
                        label = f"Ultra {height}p"
                        icon = "🌟"
                    
                    if fps:
                        label += f" {fps}fps"
                    if filesize:
                        size_mb = filesize / (1024 * 1024)
                        label += f" {size_mb:.0f}MB"
                    
                    key = f"{height}_{fps}"
                    if key not in seen:
                        seen.add(key)
                        video_formats.append({
                            'label': label,
                            'format_id': format_id,
                            'height': height,
                            'icon': icon,
                        })
            
            video_formats.sort(key=lambda x: x['height'])
            return video_formats
            
    except Exception as e:
        print_style(f"   ⚠️ {str(e)[:30]}", 'gray')
        return []

# ==============================
# DOWNLOAD FUNCTIONS
# ==============================

def download_facebook(url, format_id=None):
    print_style("   🔄 Trying 5 FB APIs...", 'gray')
    api_result = extract_facebook_api(url)
    if api_result:
        print_style("   ✅ API OK!", 'green')
        result = download_direct_video(api_result['url'], api_result['title'])
        if result:
            return result
    print_style("   🔄 Fallback yt-dlp...", 'gray')
    return download_with_ytdlp(url, format_id or 'best', 'Facebook', merge_audio=True)

def download_tiktok(url, format_id=None):
    print_style("   🔄 Trying 6 TT APIs...", 'gray')
    api_result = extract_tiktok_api(url)
    if api_result:
        print_style("   ✅ API OK!", 'green')
        result = download_direct_video(api_result['url'], api_result['title'])
        if result:
            return result
    print_style("   🔄 Fallback yt-dlp...", 'gray')
    return download_with_ytdlp(url, format_id or 'best', 'TikTok', merge_audio=False)

def download_pinterest(url, format_id=None):
    print_style("   🔄 Trying 5 Pin APIs...", 'gray')
    api_result = extract_pinterest_api(url)
    if api_result:
        print_style("   ✅ API OK!", 'green')
        result = download_direct_video(api_result['url'], api_result['title'])
        if result:
            return result
    print_style("   🔄 Fallback yt-dlp...", 'gray')
    return download_with_ytdlp(url, format_id or 'best', 'Pinterest', merge_audio=True)

def download_with_ytdlp(url, format_id, platform, merge_audio=False):
    try:
        ydl_opts = {
            'outtmpl': str(TEMP_FOLDER / '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'ignoreerrors': True,
            'geo_bypass': True,
            'nocheckcertificate': True,
            'format': format_id,
            'restrictfilenames': True,
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            }
        }
        
        if merge_audio:
            print_style("   📥 Video...", 'gray')
            video_opts = ydl_opts.copy()
            video_opts['format'] = format_id
            with yt_dlp.YoutubeDL(video_opts) as ydl:
                info_v = ydl.extract_info(url, download=True)
            
            print_style("   📥 Audio...", 'gray')
            audio_opts = ydl_opts.copy()
            audio_opts['format'] = 'bestaudio/best'
            with yt_dlp.YoutubeDL(audio_opts) as ydl:
                info_a = ydl.extract_info(url, download=True)
            
            if info_v and info_a:
                title = info_v.get('title', 'video')
                clean_title = clean_filename(title)
                
                video_files = list(TEMP_FOLDER.glob("*.mp4"))
                audio_files = list(TEMP_FOLDER.glob("*.m4a")) + list(TEMP_FOLDER.glob("*.webm"))
                
                if video_files and audio_files:
                    video_file = video_files[0]
                    audio_file = audio_files[0]
                    output_file = TEMP_FOLDER / f"{clean_title}.mp4"
                    
                    if merge_audio_video(video_file, audio_file, output_file):
                        if output_file.exists():
                            print_style("   📁 Moving...", 'gray')
                            final_path = move_to_gallery(output_file)
                            return final_path
        else:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print_style("   📥 Downloading...", 'blue')
                info = ydl.extract_info(url, download=True)
                
                if info:
                    title = info.get('title', 'video')
                    ext = info.get('ext', 'mp4')
                    clean_title = clean_filename(title)
                    
                    all_files = list(TEMP_FOLDER.glob(f"*.{ext}"))
                    if all_files:
                        all_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                        temp_file = all_files[0]
                        
                        if temp_file and temp_file.exists():
                            print_style("   📁 Moving...", 'gray')
                            final_path = move_to_gallery(temp_file)
                            return final_path
        
        return None
            
    except Exception as e:
        print_style(f"   ❌ {str(e)[:60]}", 'red')
        return None

# ==============================
# MAIN APPLICATION
# ==============================

def main():
    while True:
        print_header()
        
        print_style("  Select Platform:", 'white', bold=True)
        print()
        print_style("  [1] 📘 Facebook", 'yellow')
        print_style("  [2] 🎵 TikTok", 'yellow')
        print_style("  [3] 📌 Pinterest", 'magenta')
        print_style("  [0] 🚪 Exit", 'red')
        print()
        print_separator()
        print()
        
        choice = input("  ➤ ").strip()
        print()
        
        if choice == '0':
            print_style("  👋 Goodbye!", 'yellow')
            break
        
        if choice not in ['1', '2', '3']:
            print_style("  ❌ Invalid!", 'red')
            input("\n  Press Enter...")
            continue
        
        platform_map = {'1': 'Facebook', '2': 'TikTok', '3': 'Pinterest'}
        platform_name = platform_map[choice]
        
        print_style(f"  📌 Paste {platform_name} URL:", 'white', bold=True)
        print_separator()
        url = input("  ➤ ").strip()
        print()
        
        if not url:
            print_style("  ❌ No URL!", 'red')
            input("\n  Press Enter...")
            continue
        
        print_style("  🔍 Analyzing...", 'cyan')
        print_separator()
        
        # TikTok: API first
        if choice == '2':
            result = download_tiktok(url)
            if result:
                print_style("\n  ✅ Complete!", 'green', bold=True)
                print_style(f"  📁 {result}", 'white')
                print_style("  📱 Open Gallery!", 'cyan')
            else:
                print_style("\n  ❌ Failed!", 'red')
                print_style("  💡 Check URL or try again", 'gray')
            
            print()
            print_separator()
            again = input("\n  Download another? (y/n): ").strip().lower()
            if again != 'y':
                print_style("\n  👋 Goodbye!", 'yellow')
                break
            continue
        
        # Facebook & Pinterest: Show quality options
        formats = get_video_formats(url, platform_name.lower())
        
        if not formats:
            print_style("  ❌ No quality found!", 'red')
            input("\n  Press Enter...")
            continue
        
        print_style("\n  📊 Qualities:", 'white', bold=True)
        print_separator()
        for i, f in enumerate(formats, 1):
            print_style(f"  {f['icon']} [{i}] {f['label']}", 'yellow')
        print_style("  [0] Cancel", 'red')
        print_separator()
        print()
        
        quality_choice = input("  ➤ Select: ").strip()
        print()
        
        if quality_choice == '0':
            print_style("  ⏹️ Cancelled!", 'yellow')
            input("\n  Press Enter...")
            continue
        
        try:
            idx = int(quality_choice) - 1
            if idx < 0 or idx >= len(formats):
                print_style("  ❌ Invalid!", 'red')
                input("\n  Press Enter...")
                continue
            selected_format = formats[idx]
        except:
            print_style("  ❌ Enter number!", 'red')
            input("\n  Press Enter...")
            continue
        
        print_style(f"  📥 Downloading {selected_format['label']}...", 'blue')
        print_separator()
        
        if choice == '1':
            result = download_facebook(url, selected_format['format_id'])
        else:
            result = download_pinterest(url, selected_format['format_id'])
        
        print()
        
        if result:
            print_style("  ✅ Complete!", 'green', bold=True)
            print_style(f"  📁 {result}", 'white')
            print_style("  📱 Open Gallery!", 'cyan')
        else:
            print_style("  ❌ Failed!", 'red')
            print_style("  💡 Try different quality", 'gray')
        
        print()
        print_separator()
        again = input("\n  Download another? (y/n): ").strip().lower()
        
