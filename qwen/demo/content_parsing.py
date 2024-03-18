import random
import re
from http import HTTPStatus
import dashscope

# 定义 API 密钥
API_KEY = 'sk-16aa6d09b6ba46699e842d5dbc89ba50'

# 定义工具列表
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_base_station_info",
            "description": "Get base station information for a given person and phone number",
            "parameters": {
                "type": "object",
                "properties": {
                    "person": {
                        "type": "string",
                        "description": "The name of the person, e.g. 张三"
                    },
                    "phone_number": {
                        "type": "string",
                        "description": "The phone number, e.g. 18812261099"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "The start date of the time range, e.g. 2023-08-15"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "The end date of the time range, e.g. 2024-03-15"
                    }
                },
                "required": [
                    "person",
                    "phone_number",
                    "start_date",
                    "end_date"
                ]
            }
        }
    }
]

def process_message(user_message):
    # 解析用户输入消息
    user_content = user_message["content"]

    # 使用正则表达式提取关键信息
    person_match = re.search(r'查(\w+)的号码(\d+)的基站信息', user_content)
    start_date_match = re.search(r'开始时间是(\d{8})', user_content)
    end_date_match = re.search(r'结束时间是(\d{8})', user_content)

    # 提取匹配到的信息
    person = person_match.group(1) if person_match else ""
    phone_number = person_match.group(2) if person_match else ""
    start_date = start_date_match.group(1) if start_date_match else ""
    end_date = end_date_match.group(1) if end_date_match else ""

    # 构建消息列表
    messages = [
        user_message,
        {
            "role": "assistant",
            "content": user_content,
            "tool_calls": [
                {
                    "function": {
                        "name": "get_base_station_info",
                        "arguments": {
                            "person": person,
                            "phone_number": phone_number,
                            "start_date": start_date,
                            "end_date": end_date
                        }
                    },
                    "id": "",
                    "type": "function"
                }
            ]
        }
    ]

    # 调用 DashScope Generation 服务
    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        api_key=API_KEY,
        messages=messages,
        tools=tools,
        seed=random.randint(1, 10000),
        result_format='message'
    )

    print(response)

    # 处理回复中的指代消解和内容补全
    assistant_reply = response['messages'][1]['content'] if 'messages' in response and len(response['messages']) > 1 else ""
    return assistant_reply

# 循环交互
if __name__ == '__main__':
    while True:
        user_input = input("用户输入: ")
        user_message = {"role": "user", "content": user_input}
        assistant_reply = process_message(user_message)
        print("助手回复:", assistant_reply)
