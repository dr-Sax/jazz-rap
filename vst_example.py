from pedalboard import Pedalboard, Reverb, load_plugin
from pedalboard.io import AudioFile
import soundfile as sf
import numpy as np

# Load a VST3 or Audio Unit plugin from a known path on disk:
# instrument = load_plugin("./VSTs/Magical8BitPlug2.vst3")
effect = load_plugin("CHOWTapeModel.vst3")
audio, sample_rate = sf.read('separated/mdx_extra/oleo/bass.mp3')
audio = audio.astype(np.float32)

start_time = 1  # 1 second
end_time = 63  # 63 seconds

# Convert time to samples
start_sample = int(start_time * sample_rate)
end_sample = int(end_time * sample_rate)

# Slice the audio
audio_section = audio[start_sample:end_sample]


print(effect.parameters.keys())
# dict_keys([
#   'sc_hpf_hz', 'input_lvl_db', 'sensitivity_db',
#   'ratio', 'attack_ms', 'release_ms', 'makeup_db',
#   'mix', 'output_lvl_db', 'sc_active',
#   'full_bandwidth', 'bypass', 'program',
# ])

# Set the "ratio" parameter to 15
effect.ratio = 15

# Render some audio by passing MIDI to an instrument:
sample_rate = 44100
# audio = instrument(
#   [Message("note_on", note=60), Message("note_off", note=60, time=5)],
#   duration=5, # seconds
#   sample_rate=sample_rate,
# )

# Apply effects to this audio:
effected = effect(audio_section, sample_rate)

# ...or put the effect into a chain with other plugins:
board = Pedalboard([effect, Reverb()])
# ...and run that pedalboard with the same VST instance!
effected = board(audio, sample_rate)

sf.write('section_effected.wav', effected, sample_rate)