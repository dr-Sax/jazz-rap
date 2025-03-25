from pydub import AudioSegment

# Load WAV file
audio = AudioSegment.from_wav("media/oleo.wav")

# Export as MP3
audio.export("media/oleo.mp3", format="mp3")