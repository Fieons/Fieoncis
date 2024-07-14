from model_api.zhipu_api import summarize_with_zhipu


def reading_assistant(book_name:str):
    print("function working:"+book_name["book_name"])



def schedule_assistant(sql_dict:object):
    import sqlite3
    # 创建连接到数据库
    conn = sqlite3.connect('stores/schedule.db')
    cursor = conn.cursor()
    executting_log = ""
    
    try:
        print(f'执行sql语句:{sql_dict["sql"]}')
        executting_log += f'执行sql语句:{sql_dict["sql"]}' + "\n"
        cursor.execute(sql_dict['sql'])
        print("执行成功！")
        executting_log += "执行成功！" + "\n" + "输出为：" + "\n"
        out_puts = cursor.fetchall()
        for out_put in out_puts:
            executting_log += f'{out_put}' + "\n"
    except Exception as e:
        executting_log += f'执行失败，失败原因：{e}'
        out_put = ""
    # 提交更改并关闭连接
    conn.commit()
    conn.close()

    return f"{executting_log}" 

    

functions_gallary = {
    "reading_assistant":reading_assistant,
    "schedule_assistant":schedule_assistant,
}