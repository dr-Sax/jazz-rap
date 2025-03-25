from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH
import os

# Define paths
AUDIO_PATH = "separated/mdx_extra/saba/vocals.wav"
OUTPUT_DIR = "media"

# Create a list of paths as required by the function
audio_paths = [AUDIO_PATH]  # Put the path in a list

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Audio file path: {os.path.abspath(AUDIO_PATH)}")
print(f"Output directory: {os.path.abspath(OUTPUT_DIR)}")

predict_and_save(
    audio_paths,            # List of audio paths
    OUTPUT_DIR,            # output directory
    True,                  # save midi
    True,                  # save model outputs
    True,                  # save notes
    True,                  # sonify predictions
    ICASSP_2022_MODEL_PATH # model path
)