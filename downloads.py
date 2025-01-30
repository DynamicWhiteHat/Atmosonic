import yt_dlp

def download_youtube_as_mp3(url, output_folder="downloads"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Example usage
url = "https://www.youtube.com/watch?v=SRLZJrs8PEI"

download_youtube_as_mp3(url)
