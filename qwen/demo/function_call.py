import random
from http import HTTPStatus
import dashscope

# Set your API key here
API_KEY = 'sk-16aa6d09b6ba46699e842d5dbc89ba50'

tools = [
    {
        "type": "function",
        "function": {
            "name": "天气获取",
            "description": "获取一个指定地点的温度",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "例如城市：深圳"
                    },
                    "unit": {
                        "type": "string",
                        "enum": [
                            "摄氏度",
                            "华氏度"
                        ]
                    },
                    "fuck": {
                        "type": "int",
                        "description": "温度高低,例如25"
                    }
                },
                "required": [
                    "location","unit","fuck"
                ]
            }
        }
    }
]


def call_with_messages():
    messages = [{'role': 'user', 'content': '广州塔附件的今天的温度为38摄氏度或者40华氏度'}]
    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        api_key=API_KEY,  # Provide your API key here
        messages=messages,
        tools=tools,
        seed=random.randint(1, 10000),  # set the random seed, optional, default to 1234 if not set
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))

if __name__ == '__main__':
    call_with_messages()
