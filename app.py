import gradio as gr
from milvus_utilities import get_out_data
from query_data import get_chain 


def demo_fun(inp):
    folder_path = 'md_files_pkl'  # 请将这里替换为您需要遍历的文件夹路径
    query = inp
    
    out_dict = get_out_data(folder_path, query)
    res_text = out_dict['result_text']
    res_file_name = out_dict['result_file_name']
    
    prompt_input_mapping= {
        'result_text': res_text,
        'result_file_name': res_file_name,
        'question': query
    }

    chain = get_chain()
    o = chain.run(prompt_input_mapping)
    print(o)
    
    return o

demo = gr.Interface(fn=demo_fun, inputs="text", outputs="text")
demo.launch()