# gradio interface

import gradio as gr
from baidu_api import read_with_ernie
from googletrans import Translator
import pandas as pd

# 创建原文和翻译列表，为全局变量，用于后续操作
content_list_raw = []
content_list_translated = []
content_list_comment = []

def upload_raw_files(files):
    #上传原文
    for file in files:
        with open(file.name, 'r') as f:
            content = f.read()
            #global 需要在函数内声明
            global content_list_raw
            content_list_raw = content.split("\n")
            for i in content_list_raw:
                if i =="":
                    content_list_raw.remove(i)
            #使用html标签包裹，添加滚动条，避免文本过长下拉的时候拖动整个页面，max-height参数设置最大高度
            content_with_htmltag = "<div style='max-height: 800px; overflow-y: auto;'>"+content+"</div>"
        f.close()
    return content_with_htmltag, len(content_list_raw)

def clean_temp_file():
    #清除原文显示
    markdown_content_output = ""
    content_list_len = 0
    global content_list_raw
    content_list_raw = []
    return markdown_content_output, content_list_len

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

def input_change(inp_text):
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

def pre_paragraph(cur_paragraph_index):
    # gr.Text()组件会把数字转为str，要进行运算需要转回int
    try:
        cur_paragraph_index = int(cur_paragraph_index) - 1
        inp = content_list_raw[cur_paragraph_index]
        text_translated = content_list_translated[cur_paragraph_index]
        comment = content_list_comment[cur_paragraph_index]
        pre_next_msg = "段落索引正常"
        accept_msg = ""
    except Exception as e:
        pre_next_msg = str(e)
        cur_paragraph_index = 0
        inp = ""
        text_translated = ""
        accept_msg = ""
    return cur_paragraph_index, inp, text_translated, comment, pre_next_msg, accept_msg

def next_paragraph(cur_paragraph_index):
    # gr.Text()组件会把数字转为str，要进行运算需要转回int
    try:
        cur_paragraph_index = int(cur_paragraph_index) + 1
        inp = content_list_raw[cur_paragraph_index]
        text_translated = content_list_translated[cur_paragraph_index]
        comment = content_list_comment[cur_paragraph_index]
        pre_next_msg = "段落索引正常"
        accept_msg = ""
    except Exception as e:
        pre_next_msg = str(e)
        cur_paragraph_index = 0
        inp = ""
        text_translated = ""
        accept_msg = ""
    return cur_paragraph_index, inp, text_translated, comment, pre_next_msg, accept_msg

def translate(input_text):
    translator = Translator()
    translated_text = translator.translate(input_text, dest='zh-CN').text
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



with gr.Blocks() as demo: 
    
    gr.Markdown("工作区域")
    
    with gr.Row():
        with gr.Box():
            with gr.Column(scale=1):
                with gr.Row():
                    # 创建翻译表格按钮
                    gr.Markdown("注意！制作表格时，会将所有译文变为空字符！")
                with gr.Row():    
                    make_trans_btn = gr.Button("制作翻译表格")
                    input_trans_table_path = gr.Text(label="填入翻译表格的绝对路径")
                    make_table_output_text = gr.Markdown()
                with gr.Row():    
                    # 导入翻译表格按钮
                    # 需要使用file_count指明是单个文件，不然导入函数时文件对象是list
                    import_translated_file_btn = gr.Button("导入翻译表格")
                    output_translated_file_btn = gr.Button("导出翻译表格")  
                    files_handling_msg = gr.Markdown()
                with gr.Row():
                    cur_paragraph_index = gr.Text(label="当前段落索引")
                    content_list_len = gr.Text(label="段落总数")
                    msg = gr.Markdown()
                    pre_next_msg = gr.Markdown()
                with gr.Row():
                    inp = gr.Textbox(label="原文")
                with gr.Row():
                    #gr.Textbox组件要在后面被作为输入才能直接在textbox编辑，如我在accept_btn.click中把text_translated作为输入
                    text_translated = gr.Textbox(label="译文", editable=True)  
                with gr.Row():
                    comment = gr.Textbox(label="备注", editable=True) 
                with gr.Row():
                    pre_paragraph_btn = gr.Button("上一段")
                    next_paragraph_btn = gr.Button("下一段")
                with gr.Row():
                    tran_btn = gr.Button("翻译")
                    accept_btn = gr.Button("Accept")
                with gr.Row():
                    accept_msg = gr.Markdown()
                    
                
                # 存放各种按钮函数
                make_trans_btn.click(fn=make_trans_talbe, inputs=input_trans_table_path, outputs=make_table_output_text)
                import_translated_file_btn.click(fn=import_translated_file, inputs=input_trans_table_path, outputs= files_handling_msg)
                inp.change(fn=input_change, inputs = inp, outputs=[cur_paragraph_index, msg, text_translated])
                pre_paragraph_btn.click(fn=pre_paragraph, inputs=cur_paragraph_index, outputs=[cur_paragraph_index, inp, text_translated, comment, pre_next_msg, accept_msg])
                next_paragraph_btn.click(fn=next_paragraph, inputs=cur_paragraph_index, outputs=[cur_paragraph_index, inp, text_translated, comment, pre_next_msg,accept_msg])
                tran_btn.click(fn=translate, inputs=inp, outputs=text_translated)
                accept_btn.click(fn=accept, inputs=[cur_paragraph_index, text_translated, comment], outputs=accept_msg)
                output_translated_file_btn.click(fn=output_translated_file, inputs=input_trans_table_path, outputs=files_handling_msg)

        with gr.Box():
            with gr.Column(scale=1):
                
                # 创建上传原文按钮
                upload_raw_button = gr.UploadButton("导入原文", file_count ="multiple")
                # 创建清除按钮
                clean_button = gr.Button("Clean Up")
                
                # 创建markdown输出组件
                markdown_content_output = gr.Markdown("content")
                
                # 上传和清除按钮的函数、输入和输出
                upload_raw_button.upload(fn=upload_raw_files, inputs=upload_raw_button, outputs=[markdown_content_output, content_list_len])
                clean_button.click(fn=clean_temp_file, outputs= [markdown_content_output, content_list_len])
    
    with gr.Box():
        with gr.Row():
            gr.Markdown("与文心一言合作的区域")
        
        with gr.Row():
            with gr.Column(scale=1):
                with gr.Row():
                    question = gr.Textbox(label="提问")
                    ask_btn = gr.Button("问文心一言")
                with gr.Row():
                    anser = gr.Markdown()
        
            with gr.Column(scale=1):
                raw_text = gr.TextArea(label="原文")
            
        ask_btn.click(fn=co_with_ernie, inputs=[question, raw_text], outputs=anser)
        
    
demo.launch()