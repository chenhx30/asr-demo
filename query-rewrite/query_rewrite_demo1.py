import random
from http import HTTPStatus
import dashscope

# Set your API key here
API_KEY = 'sk-16aa6d09b6ba46699e842d5dbc89ba50'

def call_with_messages():
    # prompt = """
    # Your Task (only questions and responses are given):
    # Context:
    # Question: What was the basis of the Watergate scandal?
    # Response: ...
    # Question: …
    # Response: …
    # …
    # Current Question: So what happened to Nixon?
    # Rewrite: So what happened to Nixon after the events of the Watergate scandal?
    #
    # (Now, you should give me the rewrite and an informative response of the **Current
    # Question** based on the **Context**. The output format should always be:{
    #     Rewrite: $Reason.
    #     So the question should be rewritten as: $Rewrite.
    #     Response: $Response.
    # }
    # Go ahead!)
    # """

    # prompt = """
    # 我会给你一些例子，这些例子告诉你，需要对每次input的输入文本根据上下文进行指代消解和时间内容的补全，如果不需要进行代词替换和时间内容补全就原文返回即可
    #
    # Example #1:
    # ```
    # input: 我是张三，他是李四
    # rewrite: 这是第一回合，因为输入文本不需要进行代词替换和时间内容补全，所以原文返回即可
    # output: 我是张三，他是李四
    #
    # input: 找找他的父亲的照片
    # rewrite: 这是第二回合，因为输入文本中的第一个代词'他'指代的是第一回合中的'李四',所以需要将'他'替换为'李四'
    # output: 找找李四的父亲的照片
    #
    # input: 去年中秋到现在的所有照片
    # rewrite: 这是第三回合，因为输入文本中涉及时间内容，所以需要结合先前回合的输入输出进行内容补全
    # output: 找找李四的父亲去年中秋到现在的所有照片
    #
    # ...
    #
    # ```
    #
    # Example #2:
    # ```
    # input: 找找张三的房子在哪个村
    # rewrite: 这是第一回合，因为输入文本不需要进行代词替换和时间内容补全，所以原文返回即可
    # output: 找找张三的房子在哪个村
    #
    # input: 开始时间是2023中秋，结束时间是现在
    # rewrite: 这是第二回合，因为输入文本中涉及时间内容，所以需要结合先前回合的输入输出进行内容补全
    # output: 找找张三2023年8月15号到2024年3月27日的房子在哪个村
    #
    # ...
    #
    # ```
    #
    # ...
    #
    # 你的任务 (仅对输入input进行涉及指代消解和时间内容的改写，不涉及的原文返回):
    # Context:
    # ```
    # input: 老李的女儿真可爱
    # output: 老李的女儿真可爱
    # input: 他的女儿才三岁
    # output: 老李的女儿才三岁
    # input: 找找他的女儿的照片
    # output: 找找老李的女儿的照片
    # ```
    #
    # Current input: 帮我查一查王欧小美女去年中秋到现在的手机sjfkgj信息
    # Rewrite: 重写当前输入(现在, 你需要根据上下文**Context**并参考以上给出的示例Example，对当前输入**Current input**进行重写，输出格式必须为: input:$input. rewrite: $rewrite.output: $output.)
    #
    # """

    prompt = """
    For an information-seeking dialog, please help reformulate the question into rewrite that can fully express the user‘s information needs without the need of context and make the rewrite result as response to answer the question. For example:

    Example #1:
    ```
        Question: 我是张三，他是李四
        Rewrite: 这是第一回合，因为Question不涉及指代消解或时间内容，所以无需重写。So the question should be rewritten as: 我是张三，他是李四
        Response: 我是张三，他是李四
    
        Question: 找找他的父亲的照片
        Rewrite: 这是第二回合，因为Question涉及指代消解，第一个代词'他'指代的是第一回合中的'李四'，所以需要将'他'替换为'李四'。So the question should be rewritten as: 找找李四的父亲的照片
        Response: 找找李四的父亲的照片
    
        Question: 去年中秋到现在的所有照片
        Rewrite: 这是第三回合，因为Question涉及时间内容，所以需要结合先前回合的问答上下文进行上文拼接和内容补全，重新表述为重写无需上下文即可充分表达用户的信息需求。So the question should be rewritten as: 找找李四的父亲2023年8月15号到2024年3月28日的所有照片
        Response: 找找李四的父亲2023年8月15号到2024年3月28日的所有照片
    
        ...

    ```

    ...

    你的任务 (仅对Question进行涉及代词和时间的内容进行指代消解和时间内容补全，不涉及的原文返回):
    Context:
    ```
        Question: 老李的女儿真可爱
        Response: 老李的女儿真可爱
        Question: 他的女儿才三岁
        Response: 老李的女儿才三岁
        Question: 找找他的女儿的照片
        Response: 找找老李的女儿的照片
        Question: …
        Response: …
        …
    ```
    
    Current Question: 从2023年中秋节到现在
    Rewrite: 现在, 你需要根据上下文**Context**并参考以上给出的示例**Example**，对当前输入**Current Question**进行重写（其中时间格式统一处理为“yyyy年MM月dd日 HH时mm分ss秒SSS毫秒”），使得无需上下文即可充分表达用户的信息需求。The output format should always be: Rewrite: $Reason. So the question should be rewritten as: $Rewrite. Response: $Rewrite. Go ahead!
    
    """

    response = dashscope.Generation.call(
        'qwen-14b-chat',
        api_key=API_KEY,  # Provide your API key here
        prompt=prompt,
        seed=random.randint(1, 10000),
        result_format='message',
        temperature=0.3
    )
    if response.status_code == HTTPStatus.OK:
        # print(response)
        # 获取 content 的值
        content_value = response['output']['choices'][0]['message']['content']
        print("AI输出：" + content_value)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))

if __name__ == '__main__':
    call_with_messages()
