import json

orig = [
        {
          "text": "bitch",
          "start": 1.08,
          "end": 1.92,
          "confidence": 0.813
        },
        {
          "text": "With",
          "start": 2.76,
          "end": 2.92,
          "confidence": 0.984
        },
        {
          "text": "perfect",
          "start": 2.92,
          "end": 3.26,
          "confidence": 0.997
        },
        {
          "text": "all-American",
          "start": 3.26,
          "end": 4.24,
          "confidence": 0.998
        },
        {
          "text": "lips",
          "start": 4.24,
          "end": 5.18,
          "confidence": 0.977
        },
        {
          "text": "And",
          "start": 5.44,
          "end": 5.96,
          "confidence": 0.997
        },
        {
          "text": "perfect",
          "start": 5.96,
          "end": 6.3,
          "confidence": 1.0
        },
        {
          "text": "all-American",
          "start": 6.3,
          "end": 7.24,
          "confidence": 1.0
        },
        {
          "text": "hips",
          "start": 7.24,
          "end": 7.78,
          "confidence": 0.997
        },
        {
          "text": "I",
          "start": 8.78,
          "end": 8.86,
          "confidence": 0.998
        },
        {
          "text": "know",
          "start": 8.86,
          "end": 9.2,
          "confidence": 0.996
        },
        {
          "text": "my",
          "start": 9.2,
          "end": 9.76,
          "confidence": 1.0
        },
        {
          "text": "place,",
          "start": 9.76,
          "end": 10.16,
          "confidence": 0.995
        },
        {
          "text": "I",
          "start": 10.28,
          "end": 10.52,
          "confidence": 0.999
        },
        {
          "text": "know",
          "start": 10.52,
          "end": 10.88,
          "confidence": 1.0
        },
        {
          "text": "my",
          "start": 10.88,
          "end": 11.1,
          "confidence": 1.0
        },
        {
          "text": "place",
          "start": 11.1,
          "end": 11.71,
          "confidence": 0.999
        },
        {
          "text": "And this is it",
          "start": 11.71,
          "end": 12.06,
          "confidence": 0.898
        },
        {
          "text": "I",
          "start": 12.04,
          "end": 12.38,
          "confidence": 0.395
        },
        {
          "text": "don't",
          "start": 12.38,
          "end": 14.1,
          "confidence": 0.991
        },
        {
          "text": "get",
          "start": 14.1,
          "end": 14.24,
          "confidence": 0.999
        },
        {
          "text": "angry",
          "start": 14.24,
          "end": 14.92,
          "confidence": 1.0
        },
        {
          "text": "when",
          "start": 14.92,
          "end": 15.48,
          "confidence": 0.986
        },
        {
          "text": "I'm",
          "start": 15.48,
          "end": 15.88,
          "confidence": 0.771
        },
        {
          "text": "pissed",
          "start": 15.88,
          "end": 16.27,
          "confidence": 0.993
        }
]

diff = 100.98 - 1.08

for word in orig:
    word["start"] = round(word["start"] + diff,2)
    word["end"] = round(word["end"] + diff, 2)


for word in orig:
    pretty = json.dumps(word, indent = 4)
    print(pretty + ",")