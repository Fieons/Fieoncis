#files-search-milvus

import openai
from typing import List
from files_insert_milvus import get_embedding , file_collection
import numpy as np
from pymilvus import Collection
from config import *

openai.api_key = OPENAI_API_KEY
engine = EMBEDDINGS_MODEL

#这段代码首先使用您提供的 get_embedding 函数获取查询文本的嵌入向量。然后在已创建的 Milvus 集合中搜索相似的嵌入向量。
#搜索结果将按距离分数从低到高排序，最相似的文件具有最低的距离分数。
#请注意，这个示例仅返回相似文件的 ID 和分数。您可能需要将这些 ID 与您的原始数据关联起来，以获取更多有关文件的信息。

def search_similar_files(query: str, file_collection: Collection, engine: str, top_k: int = 5) -> List[dict]:
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
    
    return similar_files

file_collection.load()

# 示例：根据文本内容搜索相似文件
query_text = "印章"
similar_files = search_similar_files(query_text, file_collection, engine, top_k=5)

print("Similar files:")
for file_info in similar_files:
    print(f"File ID: {file_info['id']}, Score: {file_info['score']}")

file_collection.release()