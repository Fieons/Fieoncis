

TOOLS_OPTIONS = [
    {
        "type": "function",
        "function":{
            "name": "schedule_assistant",
            "description": '''
            我使用了如下样式创建了sqlite数据库:
            CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER,
            month INTEGER,
            day INTEGER,
            start_time TEXT,
            end_time TEXT,
            events TEXT
            )
            需要你根据对话内容，判断对日程数据做增、删、差、改中的哪种操作，并返回可执行的sqlite语句。
            ''',
            "parameters":{
                "type": "object",
                "properties":{
                    "sql":{
                        "type":"string",
                        "description":"sqlite执行的语句",
                    },
                },
                "required": ["sql"]
            },
        },
    },
]