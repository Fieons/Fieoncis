# gradio interface
import gradio as gr
from functions import *
import os
 

#这行代码我还未搞明白，之后再研究一下
os.environ["no_proxy"]='localhost,127.0.0.1:7897'


with gr.Blocks() as demo: 
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Row():
                with gr. Accordion(open=False, label="文件选择"):
                    files_path_list = gr.FileExplorer(root_dir="E:\我的坚果云\SciFi media\道格拉斯 亚当斯\银河系漫游系列\第一部 银河系漫游指南", container=True)
                    chose_file_btn = gr.Button("选中文件")
            with gr.Row():
                # 创建翻译表格按钮
                gr.Markdown("""
                            注意！\n
                            1. 开展工作前，需先导入工作表格表格（xlsx）。\n
                            2. 制作表格时，会将所有译文变为空字符！
                            """
                            )
            with gr.Row():
                file_path = gr.Text()    
            with gr.Row():    
                # 导入翻译表格按钮
                # 需要使用file_count指明是单个文件，不然导入函数时文件对象是list
                import_translated_file_btn = gr.Button("导入工作表")
                make_trans_btn = gr.Button("制作工作表") 
            with gr.Row():
                files_handling_msg = gr.Markdown()
                make_table_output_text = gr.Markdown()
            with gr.Row():
                cur_paragraph_index = gr.Number(label="当前段落索引")
                content_list_len = gr.Text(label="段落总数")
                msg = gr.Markdown()
            with gr.Row():
                inp = gr.Textbox(label="原文")
            with gr.Row():
                #gr.Textbox组件要在后面被作为输入才能直接在textbox编辑，如我在accept_btn.click中把text_translated作为输入
                text_translated = gr.Textbox(label="译文")  
            with gr.Row():
                comment = gr.Textbox(label="备注") 
            with gr.Row():
                tran_btn = gr.Button("翻译")
                send_to_chat_btn = gr.Button("发送到聊天区")
                search_paragraph_btn = gr.Button("根据原文查找段落")
                accept_btn = gr.Button("Accept")
                output_translated_file_btn = gr.Button("保存工作表") 
            with gr.Row():
                accept_msg = gr.Markdown()
                
            
    with gr.Row():
        with gr.Accordion("对话区域"):
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Row():
                        with gr.Group():
                            history_count = gr.Slider(1, 20, value=5, step=1, label="对话记忆长度", info="选择2-20之间")
                            model_option = gr.Radio(["ollama","智谱","ERNIE","MoonShot"], value="ollama", interactive=True, label="选择模型")
                            tools_list = gr.CheckboxGroup(["None", "reading_assistant", "schedule_assistant"], value="None", label="选择工具")
                    with gr.Row():
                        question = gr.Textbox(label="提问", scale=3)
                    with gr.Row():
                        msg_area = gr.Markdown()                   
                    
                    with gr.Row():
                        chat_bot = gr.Chatbot()
                    with gr.Row():
                        clean_chat_btn = gr.Button("清空对话")
                        cache_chat_btn = gr.Button("缓存对话")
                
                with gr.Column(scale=1):
                    with gr.Row():
                        raw_text = gr.TextArea(label="原文")
                    with gr.Row():
                        clean_raw_text_btn = gr.Button("清空原文")
                    with gr.Row():
                        tokens_usage = gr.JSON(label="tokens用量")
                    with gr.Row():
                        chat_cache_area = gr.Chatbot()
                    with gr.Row():
                        clean_chat_cache_btn = gr.Button("清空缓存对话")
    
    # 文件操作相关按钮
    chose_file_btn.click(fn=chose_file, inputs=files_path_list, outputs=file_path)
    make_trans_btn.click(fn=make_trans_talbe, inputs=file_path, outputs=make_table_output_text)
    import_translated_file_btn.click(fn=import_translated_file, inputs=file_path, outputs= [files_handling_msg,content_list_len])
    # 段落操作相关按钮
    search_paragraph_btn.click(fn=search_paragraph, inputs = inp, outputs=[cur_paragraph_index, msg, text_translated])
    cur_paragraph_index.change(fn=cur_paragraph_index_change, inputs=cur_paragraph_index, outputs=[msg, inp, text_translated, comment])
    tran_btn.click(fn=translate, inputs=inp, outputs=text_translated)
    accept_btn.click(fn=accept, inputs=[cur_paragraph_index, text_translated, comment], outputs=accept_msg)
    output_translated_file_btn.click(fn=output_translated_file, inputs=file_path, outputs=files_handling_msg)
    send_to_chat_btn.click(fn=send_to_chat, inputs=inp, outputs=raw_text)
    # 聊天相关按钮
    clean_raw_text_btn.click(fn=clean_raw_text, outputs=raw_text)
    clean_chat_btn.click(fn = clean_the_chat, outputs = chat_bot)
    cache_chat_btn.click(fn = cache_the_chat, inputs=chat_bot, outputs = chat_cache_area)
    clean_chat_cache_btn.click(fn = clean_the_chat_cache, outputs = chat_cache_area)

    question.submit(chat_app, inputs=[model_option, history_count, question, raw_text, chat_bot, tools_list], outputs=[question, chat_bot, tokens_usage])
    
demo.launch(share=False, 
            server_name="localhost", 
            allowed_paths=["./"])