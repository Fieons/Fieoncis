#files-search-milvus

from typing import List
import numpy as np
from pymilvus import Collection
from config import *
from utils import get_embedding
from pymilvus import Milvus, connections

engine = EMBEDDINGS_MODEL

#这段代码首先使用您提供的 get_embedding 函数获取查询文本的嵌入向量。然后在已创建的 Milvus 集合中搜索相似的嵌入向量。
#搜索结果将按距离分数从低到高排序，最相似的文件具有最低的距离分数。
#请注意，这个示例仅返回相似文件的 ID 和分数。您可能需要将这些 ID 与您的原始数据关联起来，以获取更多有关文件的信息。


def search_similar_files(query: str, engine: str, top_k: int = 5) -> List[dict]:
    
    # 连接到 Milvus 服务器
    connections.connect("default", host="localhost", port="19530")

    # 获取指定的 Collection 对象
    file_collection = Collection(name="file_collection")
    
    file_collection.load()
    print(f"file_collection 已加载")
    
    # 获取查询文本的嵌入向量
    query_embedding = get_embedding(query, engine)
    
    # 将查询嵌入向量转换为 numpy 数组
    query_embedding_np = np.array(query_embedding).reshape(1, -1)
    
    # 在 Milvus 中搜索相似嵌入向量
    search_params = {
        "metric_type": "L2",
        "params": {"nprobe": 10},
    }
    search_result = file_collection.search(query_embedding_np, "embeddings", search_params, limit=top_k)
    
    # 处理搜索结果
    similar_files = []
    for hit in search_result[0]:
        file_info = {
            'id': hit.id,
            'score': hit.distance
        }
        similar_files.append(file_info)
    
    file_collection.release()
    connections.disconnect("default")
    
    return similar_files

def files_query():
    while True:     

        try:
            query_text = str(input("\n请输入需查询的内容,退出请输入 “//”:"))
        except ValueError:
            print("输入无效，请输入正确的数字！")
            continue
        
        if query_text == "//":
            break
        else:
            # 根据文本内容搜索相似文件
            similar_files = search_similar_files(query_text, engine, top_k=5)

        print("Similar files:")
        for file_info in similar_files:
            print(f"File ID: {file_info['id']}, Score: {file_info['score']}")
