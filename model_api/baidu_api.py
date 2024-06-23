
import requests
import json
from config import *

def get_access_token(api_key:str, secret_key:str):
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
        
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def base_chat_erine(messages:list, tools_options:list):
    model = "completions_adv_pro" #ERNIE-4.0-8K-Preview-0518
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{model}?access_token=" + BAIDU_ACCEPT_TOKEN
    
    payload = json.dumps({
        "messages": messages,
        "functions": tools_options,
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    return response


if __name__ == '__main__':
    # 每隔一段时间就是get access token 一次，不然Access token expired
    ac = get_access_token("bEfmGvDbPGE6L66VzR7NLziF","BwNZ8IBCi4d97gtGL9NBMfPGZlgSaTlx")
    print(ac)