#启动模型
from transformers import AutoTokenizer , AutoModel
from milvus_utilities import get_out_data

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b",trust_remote_code = True)
model = AutoModel.from_pretrained("THUDM/chatglm-6b",trust_remote_code = True).half().cuda()

chatglm = model.eval()

fold_path = "/md_files_pkl"

query = "薪酬舞弊的调查方法"

out_data =  get_out_data(fold_path, query)

print(out_data)