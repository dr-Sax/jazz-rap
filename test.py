from pedalboard import Pedalboard, Chorus, Reverb, Bitcrush, Delay, Distortion, GSMFullRateCompressor, Gain, HighShelfFilter, LadderFilter, MP3Compressor, PitchShift, Resample, time_stretch 
from pedalboard.io import AudioFile
import soundfile as sf
import numpy as np

from pedalboard import Phaser
audio, sample_rate = sf.read('separated/mdx_extra/last_of_the_spiddyocks/vocals.mp3')
audio = audio.astype(np.float32)

start_time = 40  # 1 second
end_time = 120  # 63 seconds

# Convert time to samples
start_sample = int(start_time * sample_rate)
end_sample = int(end_time * sample_rate)

# Slice the audio
audio_section = audio[start_sample:end_sample]

# Create and apply effects to just this section
board = Pedalboard([ 
   
])

audio_section = time_stretch(input_audio = audio_section, samplerate= sample_rate, stretch_factor = 1.14)

effected_section = board(audio_section, sample_rate)

# If you want to save just this section:
sf.write('spiddyock_rap_2.wav', effected_section, sample_rate)