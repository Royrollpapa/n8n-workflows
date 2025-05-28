import os
from pathlib import Path
import requests
import logging

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

def generate_html_with_ai_for_gui(input_path, output_path):
    """
    供GUI调用的AI优化Markdown转HTML主入口
    input_path: 用户选择的md文件
    output_path: 用户选择的输出html文件
    """
    project_root = Path(__file__).parent.parent.parent
    guide_path = project_root / 'src' / 'scripts' / '演示文稿设计规范与实现指南.md'
    with open(guide_path, 'r', encoding='utf-8') as f:
        design_guide = f.read()
    with open(input_path, 'r', encoding='utf-8') as f:
        user_content = f.read()
    user_prompt = f"请将以下内容转为符合上述所有规范的HTML演示文稿：\n{user_content}\n输出完整HTML代码。"
    html_result = call_cursor_ai(design_guide, user_prompt)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_result)
    return output_path 