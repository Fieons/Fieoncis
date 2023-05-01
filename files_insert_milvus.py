#files-milvus

import openai
import logging
import time
from config import *
from typing import List

import os
import numpy as np
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)
from utils import get_embeddings


# 将文件内容转为嵌入向量
def convert_text_to_embeddings(file_contents, engine):
    embeddings_data = get_embeddings(file_contents, engine)
    embeddings = [data["embedding"] for data in embeddings_data]
    return np.array(embeddings)

# 读取文件内容
def read_files_in_directory(directory):
    file_contents = []
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
            content = f.read()
            file_contents.append(content)
    return file_contents


# 存储和索引文件内容
def store_and_index_files(directory, engine):
    # 读取文件内容
    file_contents = read_files_in_directory(directory)

    # 将文件内容转换为向量表示
    embeddings = convert_text_to_embeddings(file_contents, engine)

    # 连接到 Milvus
    connections.connect("default", host="localhost", port="19530")

    # 创建 Milvus 集合
    fields = [
        FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=len(embeddings[0]))
    ]

    schema = CollectionSchema(fields, "Files collection")
    file_collection = Collection("file_collection", schema, consistency_level="Strong")

    # 插入向量表示到 Milvus 集合
    entities = [
        embeddings.tolist()
    ]

    insert_result = file_collection.insert(entities)

    # 创建索引
    index = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 128},
    }

    file_collection.create_index("embeddings", index)

    return file_collection


# 示例：存储和索引文件
directory = "/Users/smart_boy/Desktop/未命名文件夹"  # 请将此路径更改为您的文件所在目录
engine = EMBEDDINGS_MODEL  # 请将此值更改为您的引擎 ID
file_collection = store_and_index_files(directory, engine)

