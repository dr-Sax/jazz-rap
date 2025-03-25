from pydub import AudioSegment
import os
import random

def combine_mp3_files(input_folder, output_file):
    """
    Combine all MP3 files from a folder in random order into a single MP3 file.
    
    Args:
        input_folder (str): Path to folder containing MP3 files
        output_file (str): Path for the output combined MP3 file
    """
    try:
        # Get all MP3 files from the folder
        mp3_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.mp3')]
        
        if not mp3_files:
            print("No MP3 files found in the specified folder!")
            return
        
        # Randomize the order
        random.shuffle(mp3_files)
        
        # Start with the first file
        combined = AudioSegment.from_mp3(os.path.join(input_folder, mp3_files[0]))
        print(f"Starting with: {mp3_files[0]}")
        
        # Add the rest of the files
        for mp3_file in mp3_files[1:]:
            print(f"Adding: {mp3_file}")
            audio = AudioSegment.from_mp3(os.path.join(input_folder, mp3_file))
            combined += audio
        
        # Export the combined file
        print(f"Exporting combined file to: {output_file}")
        combined.export(output_file, format="mp3")
        print("Done!")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    input_folder = "experiment"  # Replace with your folder path
    output_file = "combined_output.mp3"        # Replace with desired output path
    
    combine_mp3_files(input_folder, output_file)