import json
from moviepy import *
import os

import numpy as np

def create_rap_video(audio_path, lyrics_json_path, video_segments, output_path="allstar_remix.mp4"):
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
        audio = 'allstar.mp3', 
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
            'video_path': 'i-shot-the-sheriff-bob-marley.mp4',
            'start_time': 0.0,  # Start at the beginning of the song
            'end_time': 4.7,   # End after 10 seconds
            'video_start_time': 2.0,
            'video_end_time': 6.7
        },
        {
            'video_path': 'deputy-no-country.mp4',
            'start_time': 4.7, # Start at 10 seconds
            'end_time': 7.28,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 2.58,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'jayz-lost-one.mp4',
            'start_time': 7.28, # Start at 10 seconds
            'end_time': 9.28,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 2.0,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'donnie-arson.mp4',
            'start_time': 9.28, # Start at 10 seconds
            'end_time': 12.46,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 3.18,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'house-of-cards.mp4',
            'start_time': 12.46, # Start at 10 seconds
            'end_time': 14.32,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 1.86,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'monty-python-haggle.mp4',
            'start_time': 14.32, # Start at 10 seconds
            'end_time': 17.90,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 1.86,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'chip-on-shoulder.mp4',
            'start_time': 17.90, # Start at 10 seconds
            'end_time': 20.86,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 2.96,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'flint-faucet.mp4',
            'start_time': 20.86, # Start at 10 seconds
            'end_time': 22.28,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 1.42,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'toxic.mp4',
            'start_time': 22.28, # Start at 10 seconds
            'end_time': 23.72,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 1.64,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'rihanna-umbrella.mp4',
            'start_time': 23.72, # Start at 10 seconds
            'end_time': 26.04,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 2.32,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'rum-diary-papa-nebo.mp4',
            'start_time': 26.04, # Start at 10 seconds
            'end_time': 27.38,   # End at 20 seconds
            'video_start_time': 0.6,  # Start from 5 seconds into the original video
            'video_end_time': 1.94,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'coalescence.mp4',
            'start_time': 27.38, # Start at 10 seconds
            'end_time': 29.48,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 2.10,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'olympic-fist.mp4',
            'start_time': 29.48, # Start at 10 seconds
            'end_time': 31.12,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 1.64,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'bird-flock.mp4',
            'start_time': 31.12, # Start at 10 seconds
            'end_time': 32.40,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 1.28,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'water-drip.mp4',
            'start_time': 32.40, # Start at 10 seconds
            'end_time': 33.48,   # End at 20 seconds
            'video_start_time': 1,  # Start from 5 seconds into the original video
            'video_end_time': 2.08,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'eyes-on-the-prize.mp4',
            'start_time': 33.48, # Start at 10 seconds
            'end_time': 38.52,   # End at 20 seconds
            'video_start_time': 0.9,  # Start from 5 seconds into the original video
            'video_end_time': 5.94,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'whitney-spirals.mp4',
            'start_time': 38.52, # Start at 10 seconds
            'end_time': 42.16,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 3.64,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'supernova.mp4',
            'start_time': 42.16, # Start at 10 seconds
            'end_time': 45.98,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 3.82,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'chakras.mp4',
            'start_time': 45.98, # Start at 10 seconds
            'end_time': 47.42,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 1.44,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'terrence-howard.mp4',
            'start_time': 47.42, # Start at 10 seconds
            'end_time': 49.40,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 1.98,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'molach.mp4',
            'start_time': 49.40, # Start at 10 seconds
            'end_time': 50.52,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 1.12,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'flower-pluck.mp4',
            'start_time': 50.52, # Start at 10 seconds
            'end_time': 51.76,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 1.24,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'will-power.mp4',
            'start_time': 51.76, # Start at 10 seconds
            'end_time': 54.08,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 2.32,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'stilts.mp4',
            'start_time': 54.08, # Start at 10 seconds
            'end_time': 56.24,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 2.16,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'reroute-fearNloathing.mp4',
            'start_time': 56.24, # Start at 10 seconds
            'end_time': 58.36,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 2.12,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'crowdsurfing-pearl-jam.mp4',
            'start_time': 58.36, # Start at 10 seconds
            'end_time': 61.34,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 2.98,   # Use 10 seconds of the original video
        },
        {
            'video_path': 'earl-leaving.mp4',
            'start_time': 61.34, # Start at 10 seconds
            'end_time': 62.78,   # End at 20 seconds
            'video_start_time': 0,  # Start from 5 seconds into the original video
            'video_end_time': 1.44,   # Use 10 seconds of the original video
        },
    ]
    
    create_rap_video(
        audio_path="allstar.mp3",
        lyrics_json_path="allstar_fmt.json",
        video_segments=video_segments
    )