import json
from moviepy import *
import os

import numpy as np


def create_rap_video(audio_path, lyrics_json_path, video_segments, output_path):

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
    fonts_folder = "../fonts"

    # List all font files (assuming they have .ttf, .otf, or .TTF extensions)
    font_files = []
    for filename in os.listdir(fonts_folder):
        if filename.lower().endswith(('.ttf', '.otf')):
            font_path = os.path.join(fonts_folder, filename)
            font_files.append(font_path)

    color_clip = [(255, 0, 0, 128), (255, 255, 255, 128), (0, 0, 255, 128)]
    for i in range(len(lyrics_timed)):
        start_time = lyrics_timed[i][0]
        text = lyrics_timed[i][1]
        
        # Calculate duration based on the next lyric's timestamp
        if i < len(lyrics_timed) - 1:
            duration = lyrics_timed[i+1][0] - start_time
        else:
            duration = 2.0  # Default duration for the last lyric
        
        font_path = font_files[i % len(font_files)]
        font_size = 180
        y_pos = 0.8
        x_pos = 0.1
        bg_color = color_clip[i % 3]

        # Create the text clip
        txt_clip = TextClip(text=text, font_size = font_size, color='white', font = font_path, 
                           stroke_color='black', stroke_width=2, method='label', bg_color=bg_color)
        txt_clip = txt_clip.with_position((x_pos, y_pos), relative=True).with_duration(duration)
        txt_clip = txt_clip.with_start(start_time)
        txt_clip.resized(lambda t: 1 + 0.5 * np.sin(t * 2))
        
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
    final_clip = final_clip.subclipped(0, 122)
    
    # Write the result to a file
    final_clip.write_videofile(
        output_path, 
        codec='libx264', 
        audio = '../audio/olivia_rodrigo/all-american-bitch.mp3', 
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
            'video_path': '../video/amb-side-by-side.mp4',
            'start_time': 0,  # Start at the beginning of the song
            'end_time': 6.48,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 6.48
        },
        {
            'video_path': '../video/feather.mp4',
            'start_time': 6.48,  # Start at the beginning of the song
            'end_time': 8.48,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 2.0
        },
        {
            'video_path': '../video/corsette.mp4',
            'start_time': 8.48,  # Start at the beginning of the song
            'end_time': 12.64,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 4.16
        },
        {
            'video_path': '../video/emma_watson.mp4',
            'start_time': 12.64,  # Start at the beginning of the song
            'end_time': 18.60,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 5.96
        },
        {
            'video_path': '../video/scary-movie.mp4',
            'start_time': 18.92,  # Start at the beginning of the song
            'end_time': 27.8,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 8.88
        },
        {
            'video_path': '../video/brady-bunch-mom.mp4',
            'start_time': 27.8,  # Start at the beginning of the song
            'end_time': 29.78,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 1.98
        },
        {
            'video_path': '../video/mother-machine.mp4',
            'start_time': 29.78,  # Start at the beginning of the song
            'end_time': 33.72,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 3.94
        },
        {
            'video_path': '../video/barbie.mp4',
            'start_time': 33.72,  # Start at the beginning of the song
            'end_time': 39.92,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 6.2
        },
        {
            'video_path': '../video/patronus.mp4',
            'start_time': 39.92,  # Start at the beginning of the song
            'end_time': 42.22,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 2.3
        },
        {
            'video_path': '../video/pocket-sunshine.mp4',
            'start_time': 42.48,  # Start at the beginning of the song
            'end_time': 46.72,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 4.24
        },
        {
            'video_path': '../video/olivia.mp4',
            'start_time': 46.72,  # Start at the beginning of the song
            'end_time': 52.66,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 5.94
        },
        {
            'video_path': '../video/slap.mp4',
            'start_time': 52.66,  # Start at the beginning of the song
            'end_time': 55.68,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 2.98
        },
        {
            'video_path': '../video/millie-age.mp4',
            'start_time': 55.68,  # Start at the beginning of the song
            'end_time': 58.94,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 3.26
        },
        {
            'video_path': '../video/womens-march.mp4',
            'start_time': 58.94,  # Start at the beginning of the song
            'end_time': 62.84,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 3.9
        },
        {
            'video_path': '../video/amb-side-by-side.mp4',
            'start_time': 62.84,  # Start at the beginning of the song
            'end_time': 64.48,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 1.64
        },
        {
            'video_path': '../video/galadriel-lotr.mp4',
            'start_time': 64.48,  # Start at the beginning of the song
            'end_time': 66.66,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 2.18
        },
        {
            'video_path': '../video/perfume-fresh-air.mp4',
            'start_time': 66.66,  # Start at the beginning of the song
            'end_time': 70.62,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 3.96
        },
        {
            'video_path': '../video/coca-cola-hair.mp4',
            'start_time': 70.62,  # Start at the beginning of the song
            'end_time': 76.86,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 6.24
        },
        {
            'video_path': '../video/roman-holiday.mp4',
            'start_time': 76.86,  # Start at the beginning of the song
            'end_time': 78.76,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 1.9
        },
        {
            'video_path': '../video/kennedy.mp4',
            'start_time': 78.76,  # Start at the beginning of the song
            'end_time': 83.5,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 4.59
        },
        {
            'video_path': '../video/donnie-love.mp4',
            'start_time': 83.5,  # Start at the beginning of the song
            'end_time': 89.7,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 6.2
        },
        {
            'video_path': '../video/amb-side-by-side.mp4',
            'start_time': 89.7,  # Start at the beginning of the song
            'end_time': 95.98,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 6.28
        },
        {
            'video_path': '../video/resist-fox.mp4',
            'start_time': 95.98,  # Start at the beginning of the song
            'end_time': 99.88,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 3.9
        },
        {
            'video_path': '../video/amb-side-by-side.mp4',
            'start_time': 99.88,  # Start at the beginning of the song
            'end_time': 102.66,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 2.58
        },
        {
            'video_path': '../video/lips-grid.mp4',
            'start_time': 102.66,  # Start at the beginning of the song
            'end_time': 105.34,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 2.68
        },
        {
            'video_path': '../video/hips-grid.mp4',
            'start_time': 105.34,  # Start at the beginning of the song
            'end_time': 108.68,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 3.34
        },
        {
            'video_path': '../video/my-place1.mp4',
            'start_time': 108.68,  # Start at the beginning of the song
            'end_time': 110.18,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 1.5
        },
        {
            'video_path': '../video/and-this-is-it.mp4',
            'start_time': 110.18,  # Start at the beginning of the song
            'end_time': 111.61,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 1.43
        },
        
        {
            'video_path': '../video/my-place2.mp4',
            'start_time': 111.61,  # Start at the beginning of the song
            'end_time': 111.96,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 0.33
        },

        {
            'video_path': '../video/angry-pissed.mp4',
            'start_time': 111.94,  # Start at the beginning of the song
            'end_time': 116.28,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 4.34
        },
    
        {
            'video_path': '../video/knope-optimist.mp4',
            'start_time': 116.28,  # Start at the beginning of the song
            'end_time': 119.34,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 3.06
        },
        {
            'video_path': '../video/scream-inside.mp4',
            'start_time': 119.12,  # Start at the beginning of the song
            'end_time': 121.8,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 2.68
        },
        {
            'video_path': '../video/cassie-cry.mp4',
            'start_time': 146.52,  # Start at the beginning of the song
            'end_time': 150.12,   # End after 10 seconds
            'video_start_time': 0.0,
            'video_end_time': 3.6
        },
    ]
    
    create_rap_video(
        audio_path="../audio/olivia_rodrigo/all-american-bitch.mp3",
        lyrics_json_path="amb_transcript_fmt.json",
        video_segments=video_segments,
        output_path="amb-vid.mp4"
    )