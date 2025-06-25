import yt_dlp
from yt_dlp.utils import download_range_func
import os
import json

def yt_vid_downloader(st, et, name, link, fmt, format_id=None):
    start_time = st[0] * 60 + st[1]
    end_time = et[0] * 60 + et[1]
    
    # Create output path
    output_dir = 'C:/Users/nicor/OneDrive/Documents/Code/jazz-rap/media/megan-vid'
    output_file = f'{name}.{fmt}' if fmt == 'mp4' else f'{name}.wav'
    full_path = os.path.join(output_dir, output_file)
    
    # Create metadata JSON file
    metadata = {
        'source_link': link,
        'start_time': f"{st[0]}m{st[1]}s",
        'end_time': f"{et[0]}m{et[1]}s"
    }
    
    # Save metadata to a JSON file
    metadata_path = f"{os.path.splitext(full_path)[0]}_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)
    
    print(f"Saved metadata to {metadata_path}")
    
    # First list formats if no format_id is provided
    if format_id is None:
        with yt_dlp.YoutubeDL({'listformats': True}) as ydl:
            info = ydl.extract_info(link, download=False)
            print(f"Available formats for {link}:")
            for format in info.get('formats', []):
                format_id = format.get('format_id', 'N/A')
                format_note = format.get('format_note', 'N/A')
                ext = format.get('ext', 'N/A')
                resolution = format.get('resolution', 'N/A')
                vcodec = format.get('vcodec', 'N/A')
                acodec = format.get('acodec', 'N/A')
                print(f"Format ID: {format_id}, Ext: {ext}, Resolution: {resolution}, " +
                      f"Video: {vcodec}, Audio: {acodec}")
            
            print("\nPlease run the script again with a specific format_id parameter.")
            return
    
    # Common options with metadata
    yt_opts = {
        'verbose': True,
        'download_ranges': download_range_func(None, [(start_time, end_time)]),
        'force_keyframes_at_cuts': True,
        'outtmpl': full_path,
        'postprocessor_args': {
            'ffmpeg': [
                '-metadata', f'source_link={link}',
                '-metadata', f'start_time={st[0]}m{st[1]}s',
                '-metadata', f'end_time={et[0]}m{et[1]}s',
            ]
        },
        # This ensures audio and video are merged
        'merge_output_format': 'mp4',  
    }
    
    # Set format based on format_id or format type
    if format_id:
        yt_opts['format'] = format_id
    elif fmt == 'mp4':
        # Explicitly ask for both video and audio
        yt_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best'
    elif fmt == 'wav':
        yt_opts['format'] = 'bestaudio/best'
        yt_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }]
    
    # Download the file
    try:
        with yt_dlp.YoutubeDL(yt_opts) as ydl:
            ydl.download([link])
        print(f"Successfully downloaded {full_path} with metadata")
        
        # Verify the file exists
        if os.path.exists(full_path):
            print(f"Verified file exists at: {full_path}")
            print(f"File size: {os.path.getsize(full_path) / (1024*1024):.2f} MB")
        else:
            print(f"Warning: File was not found at {full_path} after download")
    
    except yt_dlp.utils.DownloadError as e:
        print(f"Download error: {e}")
        print("Try using one of the format IDs listed above")

# Example usage
ST = [1, 1]  # Start time [minutes, seconds]
ET = [1, 17]  # End time [minutes, seconds]
NAME = 'lightplay'  # Changed name to avoid overwriting
LINK = 'https://www.youtube.com/watch?v=syRbg4bwvWM'
FMT = 'mp4'

# For 720p with audio:
yt_vid_downloader(ST, ET, NAME, LINK, FMT, format_id="232+233")