import json

quiz_data = []

with open('quiz/quiz_data.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)