import requests
import pyperclip
import deepl
import re
import sys


DEEPL_API_KEY = ''
NOTION_API_KEY = ''
NOTION_PAGE_URL = ''
NOTION_DATABASE_ID = NOTION_PAGE_URL.split('-')[-1].split('/')[0].split('?pvs')[0]

source_lang = "EN"
target_lang = "JA"


def add_newlines(text):
    pattern = r'\.(?<!Fig\.)(?<!Eq\.)(?<!Sec\.)(?<!et al\.)(?=\s+[^a-z]|$)'
    replaced_text = re.sub(pattern, '.\n', text)
    cleaned_text = '\n'.join(line.lstrip() for line in replaced_text.split('\n'))
    return cleaned_text

def send_to_notion(english_sentence, japanese_sentence):
    url = f'https://api.notion.com/v1/blocks/{NOTION_DATABASE_ID}/children'
    headers = {
        'Authorization': f'Bearer {NOTION_API_KEY}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }
    data = {
        "children": [
            {
                "object": "block",
                "type": "column_list",
                "column_list": {
                    "children": [
                        {
                            "object": "block",
                            "type": "column",
                            "column": {
                                "children": [
                                    {
                                        "object": "block",
                                        "type": "paragraph",
                                        "paragraph": {
                                            "rich_text": [
                                                {
                                                    "type": "text",
                                                    "text": {
                                                        "content": english_sentence
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "object": "block",
                            "type": "column",
                            "column": {
                                "children": [
                                    {
                                        "object": "block",
                                        "type": "paragraph",
                                        "paragraph": {
                                            "rich_text": [
                                                {
                                                    "type": "text",
                                                    "text": {
                                                        "content": japanese_sentence
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        ]
    }

    response = requests.patch(url, headers=headers, json=data)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.json()}')

def split_send(english_sentence):
    max_length = 1000
    new_line_list = [i.start() for i in re.finditer("\n", english_sentence)]
    
    splitted_line = [0]
    prev_index = 0

    for i in range(len(new_line_list)):
        if new_line_list[i] - prev_index > max_length:
            splitted_line.append(new_line_list[i -1])
            prev_index = new_line_list[i -1]
    
    splitted_line.append(len(english_sentence))
    
    split_text_list = []
    for i in range(len(splitted_line)):
        if i == len(splitted_line) - 1:
            continue
        else:
            text = english_sentence[splitted_line[i]:splitted_line[i+1]]
            split_text_list.append(text)

    for text_chunk in split_text_list:
        result = translator.translate_text(text_chunk, source_lang=source_lang, target_lang=target_lang)
        japanese_sentence = result.text
        send_to_notion(text_chunk, japanese_sentence)
        print(f"Processing chunk with length {len(text_chunk)}")
        
text = pyperclip.paste()

split = None
if len(sys.argv) > 1:
    split = sys.argv[1]

if split == "split":
    print("現在の文字数：", len(text))
    while True:
        print("spaceを押すとコピーした文章を追加します")
        a = input()
        if a == " ":
            text += "\n"
            text += pyperclip.paste()
            print("現在の文字数：", len(text))
        else:
            break

new_line_list = [i.start() for i in re.finditer("\n", text)]
new_text = ""
st = 0

for i in new_line_list:
    new_text += text[st:i]
    new_text += " "
    st = i+1
new_text += text[st:]

translator = deepl.Translator(DEEPL_API_KEY)
english_sentence = add_newlines(new_text)

split_send(english_sentence)