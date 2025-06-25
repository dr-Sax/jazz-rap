import json
from moviepy import *
import os

import numpy as np

def create_rap_video(audio_path, lyrics_json_path, video_segments, output_path):
    """
    Create a video that synchronizes multiple video clips with audio and displays lyrics.
    
    Parameters:
    -----------
    audio_path : str
        Path to the audio file (.wav)
    lyrics_json_path : str
        Path to the timestamped lyrics JSON file
    video_segments : list of dict
        List of dictionaries with keys:
        - 'video_path': path to the video file
        - 'start_time': when to start this video segment in the final video (in seconds)
        - 'end_time': when to end this video segment (in seconds)
    output_path : str
        Path where the output video will be saved
    """
    # Load the audio
    audio = AudioFileClip(audio_path)
    
    # Load the lyrics
    with open(lyrics_json_path, 'r') as f:
        lyrics_data = json.load(f)
    
    # Convert the lyrics data to a list of (time, text) tuples
    lyrics_timed = [(float(time), text) for time, text in lyrics_data.items()]
    lyrics_timed.sort(key=lambda x: x[0])  # Sort by timestamp
    
    # Create a sequence of text clips for the lyrics
    text_clips = []

    # Path to your fonts folder
    fonts_folder = "fonts"

    # List all font files (assuming they have .ttf, .otf, or .TTF extensions)
    font_files = []
    for filename in os.listdir(fonts_folder):
        if filename.lower().endswith(('.ttf', '.otf')):
            font_path = os.path.join(fonts_folder, filename)
            font_files.append(font_path)

    for i in range(len(lyrics_timed)):
        start_time = lyrics_timed[i][0]
        text = lyrics_timed[i][1]
        
        # Calculate duration based on the next lyric's timestamp
        if i < len(lyrics_timed) - 1:
            duration = lyrics_timed[i+1][0] - start_time
        else:
            duration = 2.0  # Default duration for the last lyric
        
        font_path = font_files[i % len(font_files)]
        font_size = 50 * np.cos(2*np.pi * (i % len(font_files)) / len(font_files)) + 115
        x_pos = 0.25 * np.cos(2*np.pi * (i % len(font_files)) / len(font_files)) + 0.35
        y_pos = 0.25 * np.sin(2*np.pi * (i % len(font_files)) / len(font_files)) + 0.5
        # Create the text clip
        txt_clip = TextClip(text=text, font_size = font_size, color='white', font = font_path, 
                           stroke_color='black', stroke_width=2, method='label')
        txt_clip = txt_clip.with_position((x_pos, y_pos), relative=True).with_duration(duration)
        txt_clip = txt_clip.with_start(start_time)
        
        text_clips.append(txt_clip)
    
    # Get the total duration of the audio
    audio_duration = audio.duration
    
    # Create a black background for the entire duration
    background = ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=audio_duration)
    background = background.with_audio(audio)
    
    # Process video segments
    video_clips = []
    for segment in video_segments:
        video_path = segment['video_path']
        start_time = segment['start_time']
        end_time = segment['end_time']
        
        # Load the video
        video = VideoFileClip(video_path)
        
        # Trim the video if needed
        if 'video_start_time' in segment and 'video_end_time' in segment:
            video = video.subclipped(segment['video_start_time'], segment['video_end_time'])
        
        # Resize the video to fit the frame while maintaining aspect ratio
        video = video.resized(height=1080)
        
        # Position the video in the center
        video = video.with_position('center')
        
        # Set the start and end times in the final video
        video = video.with_start(start_time).with_end(end_time)
        
        # Add the video to the list
        video_clips.append(video)
    
    # Combine everything
    final_clip = CompositeVideoClip([background] + video_clips + text_clips)
    
    # Write the result to a file
    final_clip.write_videofile(
        output_path, 
        codec='libx264', 
        audio = 'the_circus.mp3', 
        fps=24,
        audio_bitrate="192k",   # Specify a standard bitrate
        temp_audiofile="temp-audio.m4a",  # Use m4a extension for temp file
        remove_temp=True,
        ffmpeg_params=["-strict", "-2"]
        )
    
    # Close all clips to free up resources
    audio.close()
    background.close()
    for clip in text_clips:
        clip.close()
    for clip in video_clips:
        clip.close()
    final_clip.close()
    
    print(f"Video successfully created at {output_path}")

# Example usage:
if __name__ == "__main__":

    # Define video segments
    video_segments = [
        {
            'video_path': 'The_circus_with_trails.mp4',
            'start_time': 0.0,  # Start at the beginning of the song
            'end_time': 76.0,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 76.0
        },
    ]
    
    create_rap_video(
        audio_path="the_circus.mp3",
        lyrics_json_path="the_circus_fmt.json",
        video_segments=video_segments,
        output_path="the_circus_trails_text.mp4"
    )