# 百度平台的api

import requests
import json
import gradio as gr


def apply_ernie(text_for_input:str):
        
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + Access_Token
    
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "我有一段英文，需要翻译为中文"
            },
            {
                "role": "assistant", 
                "content": "好的，请你将这段英文提供给我，我将为你翻译为中文。"
            },
            {
                "role": "user",
                "content": text_for_input
            }
        ],
        "temperature" : 0.9
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    return json.loads(response.text)

def translate_with_ernie(text_for_translate: str, Access_Token:str):
    
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + Access_Token
    
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "我有一段英文，需要翻译为中文"
            },
            {
                "role": "assistant", 
                "content": "好的，请你将这段英文提供给我，我将为你翻译为中文。"
            },
            {
                "role": "user",
                "content": text_for_translate
            }
        ],
        "temperature" : 0.9
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    js = json.loads(response.text)
    
    return js["result"]

def read_with_ernie(question: str, raw_text: str, Access_Token:str):
    
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + Access_Token
    
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "我正在阅读一本书，想和你讨论一下书本的内容"
            },
            {
                "role": "assistant", 
                "content": "好的，请你将这本书的原文提供给我，我会结合你的原文和你的问题，进行回答。"
            },
            {
                "role": "user",
                "content": "这本书的原文是：" + raw_text + "/n" + "我的问题是：" + question
            }
        ],
        "temperature" : 0.9
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    js = json.loads(response.text)
    
    return js["result"]

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    有效期为30日，到期要换
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_Key, "client_secret": Secret_Key}
    
    return str(requests.post(url, params=params).json().get("access_token"))

    

if __name__ == '__main__':
    API_Key = "e0A3o3Gt9SmpUFEgzGIcG4Us"
    Secret_Key = "uMW3aB1n0zFGfEBvsOIMsOXqKtDgSvK3"
    # Access_Token 30日到期，到时要换一个
    Access_Token = "24.a4b7570eba345e10d1e52534c1a675e2.2592000.1696312073.282335-38707342"  
    
    text = "Here's what the Encyclopedia Galactica has to say about alcohol. It says that alcohol is a colourless volatile liquid formed by the fermentation of sugars and also notes its intoxicating effect on certain carbon-based life forms."

    demo = gr.Interface(fn=translate_with_ernie, inputs="text", outputs="text")
    demo.launch()