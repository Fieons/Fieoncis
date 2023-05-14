import gradio as gr
from milvus_utilities import get_out_data, get_more_info
from query_data import get_chain_for_md_query


def get_md_info(inp):
    folder_path = 'md_files_pkl'  # 请将这里替换为您需要遍历的文件夹路径
    query = inp
    
    out_dict = get_out_data(folder_path, query)
    
    prompt_input_mapping= {
    'result_text': out_dict['result_text'],
    'result_file_name': out_dict['result_file_name'],
    'question': query
    }

    chain = get_chain_for_md_query()
    answer = chain.run(prompt_input_mapping)
    
    print("the original answer is :")
    print(answer)
    
    # 清洗空白字符
    answer = repr(answer)
    
    # 因为潜入Milvus的时候是分chunk进行存储的，如果资料被切断不足以回答问题，则再将前一个chunk和后一个chunk拼接后再进行回答
    # 这样有点费token 😭
    # 打算只拼接一次就算了，不要无限制上下文拼接，会超出token限制
    if answer == "资料不足够":
        more_text = get_more_info(out_dict['result_pkl'], out_dict['result_text_pk'])
        prompt_input_mapping={
            'result_text': more_text,
            'result_file_name': out_dict['result_file_name'],
            'question': query
        }
        print("answer again:")
        answer = chain.run(prompt_input_mapping)
        print(answer)
    
    else:
        print("do not need to get more informations.")
    
    # 在终端的回复包含查到到到文件名、文章内容、gpt的回答
    answer_out = f"与问题相关的文件名：{out_dict['result_file_name']} \n " \
                 f"与问题相关的文章内容：\n " \
                 f"{out_dict['result_text']} \n" \
                 f"gpt的回答: \n " \
                 f"{answer}"

    return answer_out

demo = gr.Interface(fn=get_md_info, inputs="text", outputs="text")
demo.launch()