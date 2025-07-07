from http import client
from zhipuai import ZhipuAI
from config import *
import base64



def base_chat_zhipu(zhipu_messages:list, tools_options:list=[]):
    glm_apikey = ZHIPU_API
    
    client = ZhipuAI(api_key=glm_apikey)

    response = client.chat.completions.create(
        model="glm-4-plus",
        messages=zhipu_messages,
        tools=tools_options,
        temperature=0.95,
        # 采样温度，控制输出的随机性，必须为正数
        # 取值范围是：(0.0, 1.0)，不能等于 0，默认值为 0.95，值越大，会使输出更随机，更具创造性；值越小，输出会更加稳定或确定
        # 建议您根据应用场景调整 top_p 或 temperature 参数，但不要同时调整两个参数
        top_p=0.7,
        # 用温度取样的另一种方法，称为核取样
        # 取值范围是：(0.0, 1.0) 开区间，不能等于 0 或 1，默认值为 0.7
        # 模型考虑具有 top_p 概率质量 tokens 的结果
        # 例如：0.1 意味着模型解码器只考虑从前 10% 的概率的候选集中取 tokens
        #建议您根据应用场景调整 top_p 或 temperature 参数，但不要同时调整两个参数
    )

    return response


def write_with_zhipu(condition:str, events:str):
    glm_apikey = ZHIPU_API
    
    client = ZhipuAI(api_key=glm_apikey)

    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role":"user","content":"你好"},
            {"role":"assistant","content":"你好，我是文章改写助手"},
            {"role":"user","content":"我需要你基于我给定的条件,对事件进行改写"},
            {"role":"assistant","content":"好的，请说明条件和事件"},
            {"role":"user","content":f"条件如下：{condition}"+"/n" + f"事件如下：{events}"},
        ]
    )

    return response.choices[0].message.content, response.usage

def summarize_with_zhipu(text:str):
    glm_apikey = ZHIPU_API
    
    client = ZhipuAI(api_key=glm_apikey)

    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role":"user","content":"你好"},
            {"role":"assistant","content":"我是人工智能助手"},
            {"role":"user","content":"我需要你将我提供的原文总结到100字以内"},
            {"role":"assistant","content":"好的，请提供原文"},
            {"role":"user","content":f"原文如下：{text}"}
        ]
    )

    return response.choices[0].message.content

def text_handling_with_zhipu(raw_text:str, condition:str):
    glm_apikey = ZHIPU_API

    client = ZhipuAI(api_key=glm_apikey)
    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role":"user","content":"你好"},
            {"role":"assistant","content":"我是文本操作助手"},
            {"role":"user","content":"我需要你将我提供的原文按照我的要求进行操作"},
            {"role":"assistant","content":"好的，请提供原文和操作要求"},
            {"role":"user","content":f"原文如下：{raw_text}\n" + f"操作要求如下：{condition}"}
        ]
    )

    return response.choices[0].message.content

def read_img_with_zhipu(img_path:str, ask_text:str):
    print("使用智谱glm4v")
    client = ZhipuAI(api_key=ZHIPU_API)

    with open(img_path, "rb") as image_file:
        content = image_file.read()
        encoded_image = base64.b64encode(content).decode('utf-8')

    response = client.chat.completions.create(
        model="glm-4v",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": ask_text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": encoded_image
                        }
                    }
                ]
            }
        ],
    )
    return response.choices[0].message.content