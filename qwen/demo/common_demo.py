from dashscope import Generation


if __name__ == '__main__':
    # 创建 Generation 实例
    generator = Generation()

    # 定义提示词
    prompt = "查李四的号码18812261099的基站信息,开始时间是20230101，结束时间是20240303。"
    # 使用 dashscope.Generation.call 来生成回答
    response = generator.call(prompt)

    print(response)
