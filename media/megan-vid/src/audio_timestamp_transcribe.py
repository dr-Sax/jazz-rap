import whisper_timestamped as whisper


path = '../audio/olivia_rodrigo/amb-missing-trans.mp3'

audio = whisper.load_audio(path)

model = whisper.load_model("large-v3", device = 'cpu')
result = whisper.transcribe(model, audio, language='en')
import json
json_object = json.dumps(result, indent = 2, ensure_ascii = False)

with open("amb_transcript_missing.json", "w") as outfile:
    outfile.write(json_object)