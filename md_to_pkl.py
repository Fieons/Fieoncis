# 使用langchain 搜索Milvus数据import os

from textsplitter import ChineseTextSplitter, combine_sentences, zh_title_enhance, combine_title_paragraph
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.embeddings import HuggingFaceHubEmbeddings
from langchain.vectorstores import Milvus
import os
import json
from config import *

# 构建Milvus数据库collection
# 导入目标md文件
# 返回一个tuple，（向量数据库实例，文件名，文件扩展名，connection配置）

# Load and unstructure markdown files
def loader_markdown_files(mdpath:str):
    loader = UnstructuredMarkdownLoader(mdpath)
    return loader

# split file path into filename and file_extension
def split_filename(mdpath:str):
    file_name_with_extension = os.path.basename(mdpath)
    file_name , file_extension = os.path.splitext(file_name_with_extension)
    return (file_name, file_extension)


# split text with the Chinese enhance splitter and title enhance tool
# combine title and paragraph
def split_text(loader):
    textsplitter = ChineseTextSplitter(pdf=False, sentence_size=SENTENCE_SIZE)
    docs_splited = loader.load_and_split(text_splitter=textsplitter)
    zh_enhanced_docs = zh_title_enhance(docs_splited)
    docs = combine_title_paragraph(zh_enhanced_docs)

    return docs

def encode_file_name(file_name:str):
    #collection name can only contain numbers, letters and underscores
    #因此需要对文件名称（多数时候是包含中文的）进行编码，之后再解码
    encoded_file_name = ""
    for char in file_name:
        encoded_file_name += "_{:04x}".format(ord(char))
    
    return encoded_file_name

def build_vectorstore(docs, embeddings, connectionargs:dict, encoded_file_name):
    # Load Data(docs) to vectorstore
    VectorStore = Milvus.from_documents(
        docs,
        embeddings,
        collection_name = 'cn_{}'.format(encoded_file_name),    #the first character of a collection name must be an underscore or letter
        connection_args = connectionargs ,
    )
    
    return VectorStore

# 将所构建的Milvus数据库collection主要信息序列化，以备后续查询时候导航到对应的collection
def serialize_vector_store(vectorstore, file_name, file_extension, connectionargs) -> dict:
    data = {
        "collection_name": vectorstore.collection_name, 
        "fields": vectorstore.fields,
        "index_params": vectorstore.index_params,
        "search_params": vectorstore.search_params,
        "consistency_level": vectorstore.consistency_level,
        "embedding_func": vectorstore.embedding_func.__class__.__name__,
        "file_name":file_name,
        "file_type":file_extension,
        "connection_args": connectionargs,
    }
    SerializedPath = 'stores/md_files_pkl/{}.pkl'.format(file_name)
    with open(SerializedPath, "w") as f:
        json.dump(data, f)

def markdown_to_pkl(markdown_path:str, ConnectionArgs:dict, embeddings):
    # 加载markdown file
    loader = loader_markdown_files(markdown_path)
    
    # 处理文件名和文件扩展名
    filename_tup = split_filename(markdown_path)
    
    # 分割文本内容，返回docs类
    docs = split_text(loader)
    
    # 对文件名称进行编码，方便Milvus处理文件名
    encoded_file_name = encode_file_name(filename_tup(0))
    
    # 构建Milvus vector store
    vectorstore = build_vectorstore(docs=docs, embeddings=embeddings, 
                                    connectionargs=ConnectionArgs, encoded_file_name=encoded_file_name)
    
    # 对vetorstore信息序列化
    serialize_vector_store(vectorstore=vectorstore, file_name=filename_tup(0), 
                           file_extension=filename_tup(1), connectionargs=ConnectionArgs)
    
    # 处理完毕后，释放内存  
    vectorstore.col.release()
    
MarkDownPath = "/Users/smart_boy/Nutstore Files/何志勇的坚果云/审计/知识库/人事与薪酬/薪酬舞弊调查方法与防范.md"

ConnectionArgs = {"host": "192.168.0.103", "port": "19530"}

# embedding model
repo_id = "sentence-transformers/paraphrase-xlm-r-multilingual-v1"
hg_embeddings = HuggingFaceHubEmbeddings(repo_id=repo_id, huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN)

markdown_to_pkl(markdown_path=MarkDownPath, ConnectionArgs=ConnectionArgs, embeddings=hg_embeddings)
