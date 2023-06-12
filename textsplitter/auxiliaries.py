# 存放各类辅助工具

def combine_sentences(sen_num:int , docs_list:list):
    # 将指定数目多个documents合并
    new_list = []
    for i in range(0, len(docs_list), sen_num):
        for j in range(i+1, min(i+sen_num, len(docs_list))):
            docs_list[i].page_content += docs_list[j].page_content
        new_list.append(docs_list[i])
    
    return new_list