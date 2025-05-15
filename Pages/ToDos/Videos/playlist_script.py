import json
import subprocess
import argparse
from pathlib import Path

def format_duration(seconds):
    minutes = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{minutes}:{secs:02d}"

def download_playlist_json(playlist_url, json_path):
    print(f"🎬 Downloading full metadata using youtube-dl from: {playlist_url}")
    cmd = ['yt-dlp', '--cookies', 'cookies.txt', '-j', '--yes-playlist', playlist_url]
    with open(json_path, 'w', encoding='utf-8') as f:
        subprocess.run(cmd, stdout=f, check=True)
    print(f"✅ Playlist JSON saved to: {json_path}")

def generate_markdown(json_path, playlist_url, output_path):
    rows = []
    with open(json_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            title = data.get('title', 'N/A').replace('|', '-')  # prevent markdown pipe conflict
            duration = format_duration(data.get('duration', 0)) if data.get('duration') else 'N/A'
            url = data.get('webpage_url', f"https://www.youtube.com/watch?v={data.get('id', '')}")
            rows.append(f"| [{title}]({url}) | {duration} | {url} |")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# YouTube Playlist\n\n[View full playlist]({playlist_url})\n\n")
        f.write("| Title | Duration | Video URL| Status |\n")
        f.write("|-------|----------|-----------|-----------|\n")
        f.write("\n".join(rows))

    print(f"📄 Markdown file created: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert YouTube playlist to Markdown table using youtube-dl")
    parser.add_argument("playlist_url", help="YouTube playlist URL")
    parser.add_argument("--output", "-o", default="playlist.md", help="Output Markdown filename")
    parser.add_argument("--json", "-j", default="playlist.json", help="Intermediate JSON filename (optional)")

    args = parser.parse_args()

    download_playlist_json(args.playlist_url, args.json)
    generate_markdown(args.json, args.playlist_url, args.output)

