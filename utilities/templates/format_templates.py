
# 将gradio的chat_history转换为大模型api通用可接受的messages格式
def chathistory_to_messages(chat_messages:list):
    new_chat_history = []
    # list的偶数项为user,奇数项为assistant
    if len(chat_messages) == 1 :
        # 第一轮对话
        new_chat_history.append( {"role":"user","content":chat_messages[0][0]})
        return new_chat_history
    else:
        for message_list in chat_messages:
                if message_list[1]=="":
                    new_chat_history.append({"role":"user","content":message_list[0]})
                else:
                     new_chat_history.append({"role":"user","content":message_list[0]})
                     new_chat_history.append({"role":"assistant","content":message_list[1]})


    return new_chat_history

def chathistory_to_Germini_pro(chat_messages:list):
    new_chat_history = []
    # list的偶数项为user,奇数项为assistant
    if len(chat_messages) == 1 :
        # 第一轮对话
        new_chat_history.append( {"role":"user","parts":[chat_messages[0][0]]})
        return new_chat_history
    else:
        for message_list in chat_messages:
                if message_list[1]=="":
                    new_chat_history.append({"role":"user","parts":[message_list[0]]})
                else:
                     new_chat_history.append({"role":"user","parts":[message_list[0]]})
                     new_chat_history.append({"role":"model","parts":[message_list[1]]})


    return new_chat_history     