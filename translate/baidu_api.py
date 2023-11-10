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
    # 不同模型有不同的请求地址
    ERNIE_Bot_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions"
    ERNIE_Bot_4_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro"
    
    url = ERNIE_Bot_4_url + "?access_token=" + Access_Token
    
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "我正在阅读《银河系漫游指南》英文原版第一部，当中部分英文原文我不懂，我希望给你提供原文，你帮我解读原文的意思。"
            },
            {
                "role": "assistant", 
                "content": "好的，请你将这本书的英文原文提供给我，我会结合你的原文和你的问题，进行回答。"
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

def get_access_token(api_key, secret_key):
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    有效期为30日，到期要换
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": api_key, "client_secret": secret_key}
    
    return str(requests.post(url, params=params).json().get("access_token"))

    

if __name__ == '__main__':
    API_Key = "bEfmGvDbPGE6L66VzR7NLziF"
    Secret_Key = "BwNZ8IBCi4d97gtGL9NBMfPGZlgSaTlx"
    # Access_Token 30日到期，到时要换一个
    Access_Token = "24.576e05f55df15a3bf40a463956ea9862.2592000.1700917912.282335-41808988"  
    
    gtoken=get_access_token(api_key=API_Key, secret_key=Secret_Key)
    print(gtoken)