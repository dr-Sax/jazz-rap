from pydub import AudioSegment
import json

def split_audio(input_file, output_prefix, timestamps, idx):
    """
    Split an audio file into smaller segments based on timestamps.
    
    Args:
        input_file (str): Path to the input audio file
        output_prefix (str): Prefix for output files
        timestamps (list): List of tuples containing (start_time, end_time) in seconds
    """
    # Load the audio file
    audio = AudioSegment.from_file(input_file)
    
    # Process each timestamp pair
    for i, (start_time, end_time) in enumerate(timestamps):
        # Convert seconds to milliseconds
        start_ms = start_time * 1000
        end_ms = end_time * 1000
        
        # Extract the segment
        segment = audio[start_ms:end_ms]
        
        # Generate output filename
        output_file = f"separated/mdx_extra/saba/phrase1/{idx}_{output_prefix}.mp3"
        
        # Export the segment
        segment.export(output_file, format="mp3")
        print(f"Created segment: {output_file}")

# Example usage
if __name__ == "__main__":
    with open('at_rfmt.json', 'r') as file:
        data = json.load(file)
        keys = list(data.keys())  # Convert keys to list
        
        for i, key in enumerate(keys):
            # Check if we're not at the last key
            if i < len(keys) - 1:
                current_key = float(key)
                next_key = float(keys[i + 1])
                print(f"Current key: {current_key}, Next key: {next_key}")
    
                split_audio(
                    input_file="separated/mdx_extra/saba/vocals.wav",
                    output_prefix=data[str(current_key)],
                    timestamps=[(current_key, next_key)],
                    idx=i
                )