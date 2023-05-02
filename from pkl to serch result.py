#from pkl to serch result
import json
import os
import getpass
from langchain.vectorstores import Milvus
from langchain.embeddings import OpenAIEmbeddings

os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAI API Key:')

# 反序列化
def deserialize_vector_store(file_path: str) :
    with open(file_path, "r") as f:
        vector_store_dict = json.load(f)

    # 这里之后要思考下怎样根据序列信息，引入对应的embeddings模型
    embedding_func = OpenAIEmbeddings()

    vector_store = Milvus(
        embedding_function=embedding_func,
        collection_name=vector_store_dict["collection_name"],
        index_params=vector_store_dict["index_params"],
        search_params=vector_store_dict["search_params"],
        consistency_level=vector_store_dict["consistency_level"],
        connection_args=vector_store_dict["connection_args"],
    )
    return vector_store

file_path = "./md_files_pkl/生产制造业的销售审计方案.pkl"

VectorStore = deserialize_vector_store(file_path)

query = "生产"
result = VectorStore.similarity_search(query)

print(result[0])