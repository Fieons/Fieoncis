from config import *
from openai import OpenAI

def base_chat_moonshot(messages:list, tools_options:list):
    client = OpenAI(
        api_key=MOONSHOT_API_KEY,
        base_url="https://api.moonshot.cn/v1",
    )
    
    response = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages= messages,
        temperature=0.8,
        tools=tools_options,
    )

    return response

def write_with_moonshot(condition:str, events:str):
    client = OpenAI(
        api_key=MOONSHOT_API_KEY,
        base_url="https://api.moonshot.cn/v1",
    )
    
    completion = client.chat.completions.create(
    model="moonshot-v1-8k",
    messages=[
            {"role":"user","content":"你好"},
            {"role":"assistant","content":"你好，我是文章改写助手"},
            {"role":"user","content":"我需要你基于我给定的条件,对事件进行改写"},
            {"role":"assistant","content":"好的，请说明条件和事件"},
            {"role":"user","content":f"条件如下：{condition}"+"/n" + f"事件如下：{events}"},
        ],
    temperature=0.8,
    )
    
    return completion.choices[0].message.content, completion.usage