from pydub import AudioSegment
from pathlib import Path

def convert_to_wav(mp3_path):
    # Load MP3
    audio = AudioSegment.from_mp3(mp3_path)
    
    # Create WAV path
    wav_path = Path(mp3_path).with_suffix('.wav')
    
    # Export as WAV
    audio.export(wav_path, format='wav')
    
    return str(wav_path)

# Usage
mp3_path = Path(__file__).parent / "separated" / "mdx_extra" / "saba" / "vocals.mp3"
wav_path = convert_to_wav(str(mp3_path))
print(f"Converted file saved to: {wav_path}")