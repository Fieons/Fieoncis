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
                            1. 先导入原文（md)，再导入翻译表格（xlsx）,两个步骤必不可少且顺序不能倒转。\n
                            2. 制作表格时，会将所有译文变为空字符！
                            """
                            )
            with gr.Row():
                file_path = gr.Text()    
            with gr.Row():    
                # 导入翻译表格按钮
                # 需要使用file_count指明是单个文件，不然导入函数时文件对象是list
                import_raw_mdfile_btn = gr.Button("导入原文")
                import_translated_file_btn = gr.Button("导入翻译表格")
                output_translated_file_btn = gr.Button("导出翻译表格") 
                make_trans_btn = gr.Button("制作翻译表格") 
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
                search_paragraph_btn = gr.Button("根据原文查找段落")
                accept_btn = gr.Button("Accept")
            with gr.Row():
                accept_msg = gr.Markdown()
                
            
            # 文件操作相关按钮
            chose_file_btn.click(fn=chose_file, inputs=files_path_list, outputs=file_path)
            import_raw_mdfile_btn.click(fn=import_raw_mdfile, inputs=file_path, outputs=[content_list_len, msg])
            make_trans_btn.click(fn=make_trans_talbe, inputs=file_path, outputs=make_table_output_text)
            import_translated_file_btn.click(fn=import_translated_file, inputs=file_path, outputs= files_handling_msg)
            # 段落操作相关按钮
            search_paragraph_btn.click(fn=search_paragraph, inputs = inp, outputs=[cur_paragraph_index, msg, text_translated])
            cur_paragraph_index.change(fn=cur_paragraph_index_change, inputs=cur_paragraph_index, outputs=[msg, inp, text_translated, comment])
            tran_btn.click(fn=translate, inputs=inp, outputs=text_translated)
            accept_btn.click(fn=accept, inputs=[cur_paragraph_index, text_translated, comment], outputs=accept_msg)
            output_translated_file_btn.click(fn=output_translated_file, inputs=file_path, outputs=files_handling_msg)
    
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