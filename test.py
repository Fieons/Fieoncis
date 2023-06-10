#启动模型
from transformers import AutoTokenizer, AutoModel
from milvus_utilities import get_out_data
import torch

torch.cuda.empty_cache()

fold_path = "md_files_pkl"
milvus_host = "192.168.0.104"
query = "给我一个提示语生成网站"

out_data =  get_out_data(fold_path, milvus_host, query)

context = out_data["result_text"]

# 构造 Promt
prompt = f"已知信息: \n {context} \n {query}"

# 可通过cache_dir指定模型缓存的路径，以便之后复用
tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b",trust_remote_code = True, cache_dir="E:\hugging_face_cache")
model = AutoModel.from_pretrained("THUDM/chatglm-6b",trust_remote_code = True, cache_dir="E:\hugging_face_cache").quantize(4).half().cuda()

chatglm = model.eval()

# llm生成回答
r = chatglm.chat(tokenizer, prompt, history=[])
print(r[0])
