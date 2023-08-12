# 存放各类辅助工具

def combine_sentences(sen_num:int , docs_list:list):
    # 将指定数目多个documents合并
    new_list = []
    for i in range(0, len(docs_list), sen_num):
        for j in range(i+1, min(i+sen_num, len(docs_list))):
            docs_list[i].page_content += docs_list[j].page_content
        new_list.append(docs_list[i])
    
    return new_list

def combine_title_paragraph(docs_list:list):
    #将标题和段落整合在一起
    #metadata的'category'标记为ready_to_embedding
    #合并标题和段落有个不好的地方，有可能合并后太长，不适合embedding入数据库
    #适合短段落的文件，如清单类型的
    new_list = []
    for i in range(0,len(docs_list)):
        if docs_list[i].metadata['category'] == 'cn_Title':
            docs_list[i].metadata['category'] = 'ready_to_embedding'
            j = 1
            while i+j <len(docs_list) and docs_list[i+j].metadata['category'] == 'cn_Paragraph':
                docs_list[i].page_content += "\n"
                docs_list[i].page_content += docs_list[i+j].page_content
                j+=1
            
            new_list.append(docs_list[i])
    
    return new_list  
                
    