import os
import sys
from pathlib import Path
import requests
import logging
import tkinter as tk
from interactive import ConverterGUI
from ai_md_to_html import generate_html_with_ai_for_gui

CURSOR_AI_API_URL = os.environ.get('CURSOR_AI_API_URL', 'https://api.cursor.so/v1/chat/completions')
CURSOR_AI_API_KEY = os.environ.get('CURSOR_AI_API_KEY', 'YOUR_API_KEY')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def call_cursor_ai(system_prompt, user_prompt):
    headers = {
        'Authorization': f'Bearer {CURSOR_AI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "gpt-4-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 4096,
        "temperature": 0.2
    }
    response = requests.post(CURSOR_AI_API_URL, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result['choices'][0]['message']['content']

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterGUI(root)
    root.mainloop() 