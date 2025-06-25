import json

with open('the_circus_transcript.json') as trans_file:
    file_contents = json.load(trans_file)

print(type(file_contents))
segments = file_contents['segments']

with open('the_circus_transcript.json') as json_file:
    json_decoded = json.load(json_file)

for seg in segments:

    words = seg['words']

    for word in words:

        start_pos = float(word['start'])
        json_decoded[word['start']] = word['text']

with open('the_circus_fmt.json', 'w') as json_file:
    json.dump(json_decoded, json_file)