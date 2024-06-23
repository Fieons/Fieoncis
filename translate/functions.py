from baidu_api import read_with_ernie
import pandas as pd
import sys

# vscode 需要显式地声明PYTHONPATH,不然根本找不到本项目内的模块和包的路径
sys.path.append("D:\Fieoncis")
from model_api.ollama_api import base_chat_ollama

# 创建原文和翻译列表，为全局变量，用于后续操作
content_list_raw = []
content_list_translated = []
content_list_comment = []

def import_raw_mdfile(file_path):
    # 读取文件内容
    with open(file_path, 'r') as f:
        content = f.read()
        #global 需要在函数内声明
        global content_list_raw
        content_list_raw = content.split("\n")
        for i in content_list_raw:
            if i =="":
                content_list_raw.remove(i)
    f.close()
    return len(content_list_raw), "原文导入成功"


def chose_file(file_path_list):
    return file_path_list[0]

def make_trans_talbe(input_trans_table_path):
    #制作待翻译表格
    try:
        data_dic = {
            "原文": content_list_raw, 
            "译文":["" for x in content_list_raw],
            "备注":["" for x in content_list_raw]
        }
        df = pd.DataFrame(data_dic)
        # 将DataFrame写入Excel文件
        df.to_excel(input_trans_table_path, index=False)
        make_table_output_text = "制作完成!"
    except Exception as r:
        # r需要转为字符串，才能被gr.Markdown()渲染
        make_table_output_text = str(r)
    return make_table_output_text

def import_translated_file(input_trans_table_path):
    try:
        df = pd.read_excel(input_trans_table_path)
        global content_list_translated
        global content_list_comment
        content_list_translated = df['译文'].tolist()
        content_list_comment = df['备注'].tolist()
        import__file_msg = "译文导入成功！"
    except Exception as e:
        # e需要转为字符串，才能被gr.Markdown()渲染
        import__file_msg = str(e)
    return import__file_msg

def output_translated_file(input_trans_table_path):
    global content_list_translated
    global content_list_comment
    try:
        df = pd.read_excel(input_trans_table_path)
        df['译文'] = content_list_translated
        df['备注'] = content_list_comment
        df.to_excel(input_trans_table_path, index=False)
        output_file_msg = "导出成功"
    except Exception as e:
        # e需要转为字符串，才能被gr.Markdown()渲染
        output_file_msg = str(e)
    return output_file_msg

def search_paragraph(inp_text):
    text_translated = ""
    i = 0
    while i < len(content_list_raw):
        text = content_list_raw[i]
        if text  == inp_text:
            cur_paragraph_index = i
            msg = "是一个完整的段落"
            text_translated = content_list_translated[cur_paragraph_index]
            return cur_paragraph_index, msg, text_translated
        else:
            i += 1
        
    cur_paragraph_index = None
    msg = "不是一个完成的段落！！"
    return cur_paragraph_index, msg, text_translated

def cur_paragraph_index_change(cur_paragraph_index):
    try:
        inp = content_list_raw[cur_paragraph_index]
        text_translated = content_list_translated[cur_paragraph_index]
        comment = content_list_comment[cur_paragraph_index]
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
    global content_list_translated, content_list_comment
    content_list_translated[int(index)] = text_translated
    content_list_comment[int(index)] = comment
    accept_msg = "已缓存到翻译表"
    return accept_msg

def co_with_ernie(question, raw_text):
    Access_Token = "24.576e05f55df15a3bf40a463956ea9862.2592000.1700917912.282335-41808988"
    anser = read_with_ernie(question, raw_text, Access_Token)
    return anser

