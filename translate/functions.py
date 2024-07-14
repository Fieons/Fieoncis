
import pandas as pd
import sys
import json


# vscode 需要显式地声明PYTHONPATH,不然根本找不到本项目内的模块和包的路径
sys.path.append("D:\Fieoncis")
from model_api.ollama_api import base_chat_ollama
from utilities.templates.format_templates import chathistory_to_messages
from tools_utilities.FunctionsGallary import *
from tools_utilities.preprocessor import choose_preprosessor, get_tools
from config import *

datas = {
    "原文":[],
    "译文":[],
    "备注":[]
}


def chose_file(file_path_list):
    return file_path_list[0]

def make_trans_talbe(file_path):
    #制作工作表格
    with open(file_path, 'r') as f:
        content = f.read()

    content_list_raw = [x for x in content.split("\n") if x != ""]

    # 制作工作表使用局部变量即可
    datas = {
        "原文":[],
        "译文":[],
        "备注":[]
    }

    try:
        datas["原文"] = content_list_raw
        datas["译文"] = ["" for x in content_list_raw]
        datas["备注"] = ["" for x in content_list_raw]

        df = pd.DataFrame(datas)

        new_file_path = file_path.replace(".md", "_trans.xlsx")
        # 将DataFrame写入Excel文件
        df.to_excel(new_file_path, index=False)
        msg = "制作完成!"
    except Exception as r:
        # r需要转为字符串，才能被gr.Markdown()渲染
        msg = str(r)
    return msg

def import_translated_file(input_trans_table_path):
    try:
        df = pd.read_excel(input_trans_table_path)
        globals()["datas"] = df.to_dict()
        msg = "译文导入成功！"
    except Exception as e:
        # e需要转为字符串，才能被gr.Markdown()渲染
        msg = str(e)
    return msg, len(globals()["datas"]["原文"])

def output_translated_file(input_trans_table_path):
    try:
        df = pd.read_excel(input_trans_table_path)
        df['译文'] = globals()["datas"]["译文"]
        df['备注'] = globals()["datas"]["备注"]
        df.to_excel(input_trans_table_path, index=False)
        msg = "导出成功"
    except Exception as e:
        # e需要转为字符串，才能被gr.Markdown()渲染
        msg = str(e)
    return msg

def search_paragraph(inp_text):
    text_translated = ""
    i = 0
    while i < len(globals()["datas"]["原文"]):
        text = globals()["datas"]["原文"][i]
        if text  == inp_text:
            cur_paragraph_index = i
            msg = "是一个完整的段落"
            text_translated = globals()["datas"]["译文"][cur_paragraph_index]
            return cur_paragraph_index, msg, text_translated
        else:
            i += 1
        
    cur_paragraph_index = None
    msg = "不是一个完成的段落！！"
    return cur_paragraph_index, msg, text_translated

def cur_paragraph_index_change(cur_paragraph_index):
    try:
        inp = globals()["datas"]["原文"][cur_paragraph_index]
        text_translated = globals()["datas"]["译文"][cur_paragraph_index]
        comment = globals()["datas"]["备注"][cur_paragraph_index]
        msg = "段落索引正常"
    except Exception as e:
        msg = str(e)
        inp = ""
        text_translated = ""
        comment = ""
    return msg, inp, text_translated, comment


def translate(input_text):
    messages = [
        {"role": "system", "content": "You are a helpful assistant. help user to translate text to chinese, response the translated text derectly do not reply redundant text that is not relevant to the original text"},
        {"role": "user", "content": "translate this text to chinese: " + input_text}
    ]
    response = base_chat_ollama(messages)
    translated_text = response.json()['choices'][0]['message']['content']
    return translated_text

def accept(index, text_translated, comment):
    globals()["datas"]["译文"][int(index)] = text_translated
    globals()["datas"]["备注"][int(index)] = comment
    msg = "已缓存到翻译表"
    return msg

def send_to_chat(input_text:str):
    # 将原文发送到聊天区域的“原文”框
    return input_text


def clean_the_chat():
    return []

def clean_raw_text():
    return ""

def cache_the_chat(chat_history:list):
    return chat_history

def clean_the_chat_cache():
    return []


def co_with_zhipuGLM(history_count:int, message:str, raw_text:str, chat_history:list, tools_list:list):
    print("调用智谱ai")
    from model_api.zhipu_api import base_chat_zhipu
    while len(chat_history) + 1 > history_count:
        chat_history.pop(0)
    
    # 将tools list里面的function转为符合智谱读取的
    TOOLS_OPTIONS = get_tools(tools_list)

    # gradio这里的chat_history是tuple对或者list对，将user和ai放在一个tuple或者list里面
    chat_history.append((message,""))
    chat_history_ai = chat_history
    if not raw_text == "":
        messages = chathistory_to_messages(chat_history_ai)
        messages[-1] = ({"role": "system", "content": f"你是一个阅读助手，帮助user阅读《银河系漫游指南》英文原著。user会提供一段原文给你，你基于原文，针对user所提出的问题进行回答。"})
        messages.extend(
            [
                {"role": "assistant", "content": "好的，请提供原文给我，并对我提问"},
                {"role": "user", "content": f"原文:{raw_text} \n 问题：{message}"},
            ]
        )
    else:
        messages = chathistory_to_messages(chat_history_ai)

    print(f"messages:{messages}")

    response = base_chat_zhipu(messages, TOOLS_OPTIONS)

    # 若触发function call 则走以下流程
    try:
        function_name = response.choices[0].message.tool_calls[0].function.name
        args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        print(f"主流程调用工具：{function_name}")
        from tools_utilities.FunctionsGallary import functions_gallary
        function_run =functions_gallary[function_name]
        anser = function_run(args)
        usage = response.usage
        chat_history[-1] = (message, anser)
        print("本轮对话结束，对话历史：")
        print(chat_history)
        return "", chat_history, usage
    except Exception as e:
        print(f"本次无调用function call，错误：{e}")
        

    anser = response.choices[0].message.content
    usage = response.usage
    chat_history[-1] = (message, anser)

    print("本轮对话结束.")

    return "", chat_history, usage

def co_with_ollama(history_count:int, message:str, raw_text:str, chat_history:list, tools_list:list):
    print("调用ollama")
    while len(chat_history) + 1 > history_count:
        chat_history.pop(0)


    # 将tools list里面的function转为符合智谱读取的
    TOOLS_OPTIONS = get_tools(tools_list)

    # gradio这里的chat_history是tuple对或者list对，将user和ai放在一个tuple或者list里面
    chat_history.append((message,""))
    chat_history_ai = chat_history
    if not raw_text == "":
        messages = chathistory_to_messages(chat_history_ai)
        messages[-1] = ({"role": "system", "content": f"你是一个阅读助手，帮助user阅读《银河系漫游指南》英文原著。user会提供一段原文给你，你基于原文，针对user所提出的问题进行回答。"})
        messages.extend(
            [
                {"role": "assistant", "content": "好的，请提供原文给我，并对我提问"},
                {"role": "user", "content": f"原文:{raw_text} \n 问题：{message}"},
            ]
        )
    else:
        messages = chathistory_to_messages(chat_history_ai)

    print(f"messages:{messages}")

    response = base_chat_ollama(messages, TOOLS_OPTIONS)

    # 若触发function call 则走以下流程
    try:
        function_name = response.choices[0].message.tool_calls[0].function.name
        args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        print(f"主流程调用工具：{function_name}")
        from tools_utilities.FunctionsGallary import functions_gallary
        function_run =functions_gallary[function_name]
        anser = function_run(args)
        usage = response.usage
        chat_history[-1] = (message, anser)
        print("本轮对话结束，对话历史：")
        print(chat_history)
        return "", chat_history, usage
    except Exception as e:
        print(f"本次无调用function call，错误：{e}")
        

    anser = response.json()['choices'][0]['message']['content']
    usage = response.json()['usage']
    chat_history[-1] = (message, anser)

    print("本轮对话结束.")

    return "", chat_history, usage


def co_with_Ernie(history_count:int, message:str, raw_text:str, chat_history:list, tools_list:list):
    print("调用文心一言")
    from model_api.baidu_api import base_chat_erine
    while len(chat_history) + 1 > history_count:
        chat_history.pop(0)
    
    # 将tools list里面的function转为符合模型调用的
    TOOLS_OPTIONS = get_tools(tools_list)

    # gradio这里的chat_history是tuple对或者list对，将user和ai放在一个tuple或者list里面
    chat_history.append((message,""))
    chat_history_ai = chat_history
    if not raw_text == "":
        messages = chathistory_to_messages(chat_history_ai)
        messages[-1] = ({"role": "user", "content": f"你是一个阅读助手，帮助user阅读《银河系漫游指南》英文原著。user会提供一段原文给你，你基于原文，针对user所提出的问题进行回答。"})
        messages.extend(
            [
                {"role": "assistant", "content": "好的，请提供原文并向我提问。"},
                {"role": "user", "content": f"原文:{raw_text} \n 问题：{message}"},
            ]
        )
    else:
        messages = chathistory_to_messages(chat_history_ai)

    print(f"messages:{messages}")

    response = base_chat_erine(messages, TOOLS_OPTIONS)
    print(response)
    print(response.json())


    # 若触发function call 则走以下流程(Erine的function call 接口很不一样，妈的，懒得去写)
    try:
        function_name = response.choices[0].message.tool_calls[0].function.name
        args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        print(f"主流程调用工具：{function_name}")
        from tools_utilities.FunctionsGallary import functions_gallary
        function_run =functions_gallary[function_name]
        anser = function_run(args)
        usage = response.usage
        chat_history[-1] = (message, anser)
        print("本轮对话结束，对话历史：")
        print(chat_history)
        return "", chat_history, usage
    except Exception as e:
        print(f"本次无调用function call，错误：{e}")
        

    anser = response.json().get("result")
    usage = response.json().get("usage")
    chat_history[-1] = (message, anser)

    print("本轮对话结束.")

    return "", chat_history, usage

def co_with_moonshot(history_count:int, message:str, raw_text:str, chat_history:list, tools_list:list):
    print("调用MoonShot")
    from model_api.moonshot_api import base_chat_moonshot
    while len(chat_history) + 1 > history_count:
        chat_history.pop(0)
    
    # 将tools list里面的function转为符合模型调用的
    TOOLS_OPTIONS = get_tools(tools_list)

    # gradio这里的chat_history是tuple对或者list对，将user和ai放在一个tuple或者list里面
    if not raw_text == "":
        messages = chathistory_to_messages(chat_history_ai)
        messages[-1] = ({"role": "system", "content": f"你是一个阅读助手，帮助user阅读《银河系漫游指南》英文原著。user会提供一段原文给你，你基于原文，针对user所提出的问题进行回答。"})
        messages.extend(
            [
                {"role": "assistant", "content": "好的，请提供原文给我，并对我提问"},
                {"role": "user", "content": f"原文:{raw_text} \n 问题：{message}"},
            ]
        )
    else:
        message_for_ai = message

    chat_history_ai = chat_history
    chat_history_ai.append((message_for_ai,""))

    # 将chat_history转换为messages格式
    messages = chathistory_to_messages(chat_history_ai)

    response = base_chat_moonshot(messages, TOOLS_OPTIONS)

    # 若触发function call 则走以下流程
    try:
        function_name = response.choices[0].message.tool_calls[0].function.name
        args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        print(f"主流程调用工具：{function_name}")
        from tools_utilities.FunctionsGallary import functions_gallary
        function_run =functions_gallary[function_name]
        anser = function_run(args)
        usage = response.usage
        chat_history[-1] = (message, anser)
        print("本轮对话结束，对话历史：")
        print(chat_history)
        return "", chat_history, usage
    except Exception as e:
        print(f"本次无调用function call，错误：{e}")
        

    anser = response.choices[0].message.content
    usage = response.usage
    chat_history[-1] = (message, anser)

    print("本轮对话结束.")

    return "", chat_history, usage
    

def chat_app(model_option:str, history_count:int, msg:str, events:str, chat_history:list, tools_list:list):
    # 所有输入会先到这个主程序，然后再对各种参数进行调度
    print(f"第{len(chat_history)+1}轮对话--------------------------------")
    model_dic = {"智谱": co_with_zhipuGLM, "ollama": co_with_ollama, "ERNIE": co_with_Ernie, "MoonShot": co_with_moonshot}
    
    # 根据model_option的选择调动model function
    model = model_dic[model_option]
    
    # 预处理，当需要使用某些工具时，进行预处理
    msg = choose_preprosessor(msg, tools_list)

    return model(history_count, msg, events, chat_history, tools_list)