import random
from http import HTTPStatus
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role

# Set your API key here
API_KEY = 'sk-16aa6d09b6ba46699e842d5dbc89ba50'

def multi_round_conversation():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},

        {"role": "user", "content": "{'问题'：'帮我查张三的号码信息', '回答者的角色'：'通信行业的专家', '目的'：'根据上下文，对问题中的代词替换为实际名称，对问题中的时间整理为开始时间和结束时间，最后使问题描述尽可能简洁专业', '输出'：'?'}"},
        {"role": "assistant", "content": "查张三的号码信息"},

        {"role": "user", "content": "{'问题'：'查他2024年1月1号至今的号码信息', '回答者的角色'：'通信行业的专家', '目的'：'根据上下文，对问题中的代词替换为实际名称，对问题中的时间整理为开始时间和结束时间，最后使问题描述尽可能简洁专业', '输出'：'?'}"},
        {"role": "assistant", "content": "查张三2024年1月1号至2024年3月18号的号码信息"},

        {"role": "user", "content": "{'问题'：'开始时间20230101，结束时间20240202', '回答者的角色'：'通信行业的专家', '目的'：'根据上下文，对问题中的代词替换为实际名称，对问题中的时间整理为开始时间和结束时间，最后使问题描述尽可能简洁专业', '输出'：'?'}"},
        {"role": "assistant", "content": "查张三2023年1月1号至2024年2月2号的号码信息"},

        {"role": "user", "content": "{'问题'：'帮我查李四的号码信息', '回答者的角色'：'通信行业的专家', '目的'：'根据上下文，对问题中的代词替换为实际名称，对问题中的时间整理为开始时间和结束时间，最后使问题描述尽可能简洁专业', '输出'：'?'}"},
        {"role": "assistant", "content": "查李四的号码信息"},

        {"role": "user", "content": "{'问题'：'查他2024年1月1号至今的号码信息', '回答者的角色'：'通信行业的专家', '目的'：'根据上下文，对问题中的代词替换为实际名称，对问题中的时间整理为开始时间和结束时间，最后使问题描述尽可能简洁专业', '输出'：'?'}"},
        {"role": "assistant", "content": "查李四2024年1月1号至2024年3月18号的号码信息"},

        {"role": "user", "content": "{'问题'：'开始时间20230101，结束时间20240202', '回答者的角色'：'通信行业的专家', '目的'：'根据上下文，对问题中的代词替换为实际名称，对问题中的时间整理为开始时间和结束时间，最后使问题描述尽可能简洁专业', '输出'：'?'}"},
        {"role": "assistant", "content": "查李四2023年1月1号至2024年2月2号的号码信息"},

        {"role": "user", "content": "{'问题'：'帮我查王五的号码信息', '回答者的角色'：'通信行业的专家', '目的'：'根据上下文，对问题中的代词替换为实际名称，对问题中的时间整理为开始时间和结束时间，最后使问题描述尽可能简洁专业', '输出'：'?'}"}

    ]
    response = Generation.call(
        'qwen-14b-chat',
        api_key=API_KEY,  # Provide your API key here
        messages=messages,
        # set the random seed, optional, default to 1234 if not set
        seed=random.randint(1, 10000),
        result_format='message',  # set the result to be "message"  format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
        messages.append({'role': response.output.choices[0]['message']['role'],
                         'content': response.output.choices[0]['message']['content']})
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))

    messages.append({"role": "user", "content": "{'问题'：'开始时间20230201，结束时间20240302', '回答者的角色'：'通信行业的专家', '目的'：'根据上下文，对问题中的代词替换为实际名称，对问题中的时间整理为开始时间和结束时间，最后使问题描述尽可能简洁专业', '输出'：'?'}"})
    response = Generation.call(
        'qwen-14b-chat',
        api_key=API_KEY,  # Provide your API key here
        messages=messages,
        result_format='message',  # set the result to be "message"  format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))

    messages.append({'role': response.output.choices[0]['message']['role'],
                     'content': response.output.choices[0]['message']['content']})

    messages.append({"role": "user", "content": "{'问题'：'查以上3个人2023年1月6号至今的号码信息', '回答者的角色'：'通信行业的专家', '目的'：'根据上下文，对问题中的代词替换为实际名称，对问题中的时间整理为开始时间和结束时间，最后使问题描述尽可能简洁专业', '输出'：'?'}"})
    response = Generation.call(
        'qwen-14b-chat',
        api_key=API_KEY,  # Provide your API key here
        messages=messages,
        result_format='message',  # set the result to be "message"  format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


if __name__ == '__main__':
    multi_round_conversation()