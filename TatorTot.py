import os
import argparse
from yt_dlp import YoutubeDL
from tqdm import tqdm

def download_audio_from_youtube(url, output_dir):
    # Predefine filename so it's available if an exception is raised
    filename = "unknown"

    # Safe probing to get the title and intended output name
    ydl_probe_opts = {
        'quiet': False,  # Keeps yt-dlp from silently stalling
        'skip_download': True,
        'noplaylist': True,
        'socket_timeout': 10,
    }

    try:
        with YoutubeDL(ydl_probe_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get("title", "unknown")
            filename = os.path.join(output_dir, f"{title}.mp3")

        if os.path.exists(filename):
            print(f"[↷] Skipped (already exists): {filename}")
            return

        # Actual download
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'noplaylist': True,
            'socket_timeout': 10,
            'retries': 2,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print(f"[✓] Downloaded and converted: {filename}")

    except Exception as e:
        print(f"[✗] FAILED: {url}")
        print(f"    → Intended output: {filename}")
        print(f"    → Error: {str(e)}")

def load_urls(source):
    if os.path.isfile(source):
        with open(source, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    else:
        return [source]

def main():
    parser = argparse.ArgumentParser(description="Download YouTube audio as MP3.")
    parser.add_argument("source", help="YouTube URL or path to file with URLs")
    args = parser.parse_args()

    output_dir = "mp3s"
    os.makedirs(output_dir, exist_ok=True)

    urls = load_urls(args.source)
    for url in tqdm(urls, desc="Processing videos"):
        download_audio_from_youtube(url, output_dir)

if __name__ == "__main__":
    main()
