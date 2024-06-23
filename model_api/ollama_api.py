import requests
import json

def base_chat_ollama(messages:list, tools_options:list = []):
    base_ip = "127.0.0.1"

    ollama_port = "11434"

    # ollama有提供openai的api，使用v1/chat/completions调用openai的api
    base_url = f'http://{base_ip}:{ollama_port}/v1/chat/completions'

    header = {"Content-Type": "application/json"}

    selected_model = "qwen2:7b"

    data = {
            'model': selected_model, 
            'messages': messages,
            'tools': tools_options,
            'temperature': 0.9,
        }

    response = requests.post(headers=header,url=base_url, json=data)

    if response.status_code == 200:
        return response
        #content = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
        #usage = response.json().get('usage', {})

    else:
        print(f"Error: Request failed with status code {response.status_code}")
        return None


def text_handling_with_ollama(raw_text:str, ask_text:str):
    base_ip = "127.0.0.1"

    ollama_port = "11434"

    base_url = f'http://{base_ip}:{ollama_port}/v1/chat/completions'

    selected_model = "qwen:14b"

    messages = [
        {"role": "system", "content": f"我们基于如下文本进行谈话：{raw_text}，你需要根据文本及我提出的问题，直接进行回答"},
        ({"role": "user", "content": ask_text})
        ]

    data = {
            'model': selected_model, 
            'messages': messages,
            'options':{
                "temperature": 0.9,
            }
        }

    response = requests.post(url=base_url, json=data)

    if response.status_code == 200:
        return response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
        #content = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
        #usage = response.json().get('usage', {})

    else:
        print(f"Error: Request failed with status code {response.status_code}")
        return None


if __name__ == '__main__':
    pass