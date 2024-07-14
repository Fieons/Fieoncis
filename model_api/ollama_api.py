import requests
import json

def base_chat_ollama(messages:list, tools_options:list = []):
    base_ip = "127.0.0.1"

    ollama_port = "11434"

    # ollama有提供openai的api，使用v1/chat/completions调用openai的api
    base_url = f'http://{base_ip}:{ollama_port}/v1/chat/completions'

    header = {"Content-Type": "application/json"}

    selected_model = "qwen:32b"

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



if __name__ == '__main__':
    pass