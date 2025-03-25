import whisper_timestamped as whisper

import soundfile as sf
import numpy as np

path = 'media/allstar-earl/allstar.wav'


audio = whisper.load_audio(path)

model = whisper.load_model("tiny", device = 'cpu')
result = whisper.transcribe(model, audio, language='en')
import json
json_object = json.dumps(result, indent = 2, ensure_ascii = False)

with open("allstar_earl_transcript.json", "w") as outfile:
    outfile.write(json_object)