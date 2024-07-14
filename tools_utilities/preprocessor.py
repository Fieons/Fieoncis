from tools_utilities.tools_gallary import TOOLS_OPTIONS

def choose_preprosessor(msg:str, tools_name_list:list) -> str:
    # 选择预处理
    for tool in tools_name_list:
        if tool == "schedule_assistant":
            msg += date_check_preprosessor()
        elif tool =="None":
            msg += ""

    return msg

def date_check_preprosessor() -> str:
    # 日期预处理
    from datetime import datetime
    now = datetime.now()
    year = now.year
    day = now.day
    month = now.month
    weekday = now.isoweekday()
    time = now.strftime("%H:%M:%S")
    return f"（今天是{year}年{month}月{day}日,周{weekday},当前时间为:{time})"

def get_tools(tools_name_list:list):
    activated_options = []
    for tool in TOOLS_OPTIONS:
        if tool["function"]["name"] in tools_name_list:
            activated_options.append(tool)
    
    return activated_options
