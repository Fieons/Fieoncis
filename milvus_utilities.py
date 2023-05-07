#from pkl to serch result
import json
from langchain.vectorstores import Milvus
from langchain.embeddings import OpenAIEmbeddings
from config import *
import os

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# 反序列化
def deserialize_to_milvus_vectorstore(file_path: str) :
    with open(file_path, "r") as f:
        vector_store_dict = json.load(f)

    # 这里之后要思考下怎样根据序列信息，引入对应的embeddings模型
    embedding_func = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    vector_store = Milvus(
        embedding_function=embedding_func,
        collection_name=vector_store_dict["collection_name"],
        index_params=vector_store_dict["index_params"],
        search_params=vector_store_dict["search_params"],
        consistency_level=vector_store_dict["consistency_level"],
        connection_args=vector_store_dict["connection_args"],
    )
    return vector_store

# 遍历pkl文件，返回路径list，用于后续遍历所有collection以搜索最优匹配文本
def list_files(folder_path):
    file_paths = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)

    return file_paths


def search_text_from_milvus(pkl_path,query):
    vectorstore = deserialize_to_milvus_vectorstore(pkl_path)
    outtext = vectorstore.similarity_search(query)
    
    return outtext


def get_out_data(folder_path, query):
    candidate_list = []
    pkl_file_paths = list_files(folder_path)
    
    for pkl in pkl_file_paths:
        vectorstore = deserialize_to_milvus_vectorstore(pkl)
        out_tuple = vectorstore.similarity_search_with_score(query)[0]   #第一个通常是相似度最优的
        vectorstore.col.release()

        # out_tuple 为有2个值的tuple
        # 第一个是Document类，包含变量page_content和metadata两个变量和对应的值
        # 第二个是score，相似度度量的值
        file_source = out_tuple[0].metadata['source']
        file_name = os.path.basename(file_source)
    
        file_text = out_tuple[0].page_content

        file_text_score = out_tuple[1]

        candidate_list.append((file_text,file_name,file_text_score))

    sorted_list = sorted(candidate_list, key=lambda x: x[2])

    return {'result_text': sorted_list[0][0] , 'result_file_name': sorted_list[0][1]}



