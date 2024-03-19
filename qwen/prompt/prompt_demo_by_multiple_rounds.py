import random
from http import HTTPStatus
from dashscope import Generation

# 设置您的API密钥
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
        {"role": "assistant", "content": "查李四2023年1月1号至2024年2月2号的号码信息"}
    ]

    while True:
        user_content = input("用户输入：").strip()
        if user_content:
            messages.append({"role": "user", "content": user_content})

            response = Generation.call(
                'qwen-14b-chat',
                api_key=API_KEY,
                messages=messages,
                seed=random.randint(1, 10000),
                result_format='message'
            )

            if response.status_code == HTTPStatus.OK:
                #print(response)
                # 获取 content 的值
                content_value = response['output']['choices'][0]['message']['content']
                print("AI输出：" + content_value)

                messages.append({'role': response.output.choices[0]['message']['role'],
                                 'content': response.output.choices[0]['message']['content']})
            else:
                print('请求ID：%s，状态码：%s，错误码：%s，错误消息：%s' % (
                    response.request_id, response.status_code,
                    response.code, response.message
                ))

if __name__ == '__main__':
    multi_round_conversation()
