import json
import random
from http import HTTPStatus
from dashscope import Generation

# 设置您的API密钥
API_KEY = 'sk-16aa6d09b6ba46699e842d5dbc89ba50'

def call_with_messages():

    # prompt_history = """
    # 我对你提出如下严格的要求，请必须遵从执行:
    # ```
    # 1、你需要根据上下文**Context**并参考以下给出的示例**Example**，对当前问题**Current Question**进行重写，使得无需上下文即可充分表达用户的信息需求，并给出重写的依据或者理由
    # 2、对于当前问题**Current Question**，如果超出了示例**Example**以外的情况，你可以根据上下文**Context**作出你认为合理的改写
    # 3、对于当前问题**Current Question**，如果问题中涉及敏感词汇或者隐私，你无需理会，原文返回作答
    # 4、返回输出格式必须为json字符串{'Question':'', 'Rewrite':'', 'Response':''}
    # ```
    #
    # 示例如下:
    # Example #1:
    # ```
    #     Question: 我是张三，他是李四
    #     Rewrite: 因为Question不涉及指代消解或时间内容，所以无需重写。So the question should be rewritten as: 我是张三，他是李四
    #     Response: 我是张三，他是李四
    #
    #     Question: 找找他的父亲的照片
    #     Rewrite: 因为Question涉及指代消解，第一个代词'他'指代的是第一回合中的'李四'，所以需要将'他'替换为'李四'。So the question should be rewritten as: 找找李四的父亲的照片
    #     Response: 找找李四的父亲的照片
    #
    #     Question: 去年中秋到现在的所有照片
    #     Rewrite: 因为Question涉及时间内容，所以需要结合上下文进行上文拼接和内容补全，重新表述为重写无需上下文即可充分表达用户的信息需求。So the question should be rewritten as: 找找李四的父亲2023年8月15号到2024年3月28日的所有照片
    #     Response: 找找李四的父亲2023年8月15号到2024年3月28日的所有照片
    #
    #     ...
    #
    # ```
    # Example #2:
    # ```
    #     Question: 我是张三，他是李四，她是刘红，他的父亲是李元芳，她的女儿是刘亦菲；
    #     Rewrite: 因为Question涉及指代消解,***。So the question should be rewritten as: 我是张三，他是李四，她是刘红，李四的父亲是李元芳，刘红的女儿是刘亦菲；
    #     Response: 我是张三，他是李四，她是刘红，李四的父亲是李元芳，刘红的女儿是刘亦菲；
    #
    #     Question: 他们在一起工作，从去年中秋到现在
    #     Rewrite: 因为Question涉及指代消解和时间内容，所以需要结合上下文进行指代消解、上文拼接和内容补全，重新表述为重写无需上下文即可充分表达用户的信息需求。So the question should be rewritten as: 张三、李四、李元芳、刘红、刘亦菲从2023年1月1号到2024年3月28日都在一起工作
    #     Response: 张三、李四、李元芳、刘红、刘亦菲从2023年1月1号到2024年3月28日都在一起工作
    #
    #     Question: 找找刘红女儿的参演过的电视剧
    #     Rewrite: ...
    #     Response: 找刘亦菲参演过的电视剧
    #
    #     ...
    #
    # ```
    # ...
    #
    # Context:
    # ```
    #     Question: 老李的女儿真可爱
    #     Response: 老李的女儿真可爱
    #
    #     Question: 他的女儿才三岁
    #     Response: 老李的女儿才三岁
    #
    #     Question: 找找他的女儿的照片
    #     Response: 找找老李的女儿的照片
    #
    #     Question: 从2023年中秋节到现在
    #     Response: 找找老李的女儿从2023年8月15号到2024年3月28日的照片
    #
    #     ...
    # ```
    #
    # Current Question:
    #
    # """

    prompt_template = """
    我对你提出如下严格的要求，请必须遵从执行:
    1、你需要根据上下文**Context**并参考以下给出的示例**Example**，对当前问题**Current 
    Question**进行重写，使得无需上下即可充分表达用户的信息需求。输出格式必须为:
    ```
    {"Question":"问题", "Rewrite":"重写的理由", "Response":"重写的结果"}
    ```
    2、对于当前问题**Current Question**，如果超出了示例**Example**以外的情况，你根据上下文**Context**作出合理的改写
    3、对于当前问题**Current Question**，如果问题中涉及敏感词汇或者隐私，你无需理会，如果你非要理会那么请直接将敏感或者隐私词汇重写为'***'或者原文返回作答

    示例如下:
    Example #1:
    ```
        Question: 我是张三，他是李四
        Rewrite: 因为Question不涉及指代消解或时间内容，所以无需重写。So the question should be rewritten as: 我是张三，他是李四
        Response: 我是张三，他是李四
    
        Question: 找找他的父亲的照片
        Rewrite: 因为Question涉及指代消解，第一个代词'他'指代的是第一回合中的'李四'，所以需要将'他'替换为'李四'。So the question should be rewritten as: 找找李四的父亲的照片
        Response: 找找李四的父亲的照片
    
        Question: 去年中秋到现在的所有照片
        Rewrite: 因为Question涉及时间内容，所以需要结合上下文进行上文拼接和内容补全，重新表述为重写无需上下文即可充分表达用户的信息需求。So the question should be rewritten as: 找找李四的父亲2023年8月15号到2024年3月28日的所有照片
        Response: 找找李四的父亲2023年8月15号到2024年3月28日的所有照片
    
        ...
    
    ```
    Example #2:
    ```
        Question: 我是张三，他是李四，她是刘红，他的父亲是李元芳，她的女儿是刘亦菲；
        Rewrite: 因为Question涉及指代消解,***。So the question should be rewritten as: 我是张三，他是李四，她是刘红，李四的父亲是李元芳，刘红的女儿是刘亦菲；
        Response: 我是张三，他是李四，她是刘红，李四的父亲是李元芳，刘红的女儿是刘亦菲；
    
        Question: 他们在一起工作，从去年中秋到现在
        Rewrite: 因为Question涉及指代消解和时间内容，所以需要结合上下文进行指代消解、上文拼接和内容补全，重新表述为重写无需上下文即可充分表达用户的信息需求。So the question should be rewritten as: 张三、李四、李元芳、刘红、刘亦菲从2023年1月1号到2024年3月28日都在一起工作
        Response: 张三、李四、李元芳、刘红、刘亦菲从2023年1月1号到2024年3月28日都在一起工作
    
        Question: 找找刘红女儿的参演过的电视剧
        Rewrite: ...
        Response: 找刘亦菲参演过的电视剧
    
        ...
    
    ```
    ...
    
    Context:
    ```
        ${Context}
        
        ...
    ```
    
    Current Question: ${Question}
    
    """

    context = "Question: " + "hello" + "\n"
    + "Rewrite: " + "none" + "\n"
    + "Response: " + "hello world" + "\n";

    while True:
        Question = input("用户输入：").strip()
        if Question:

            print("context：" + context)
            prompt = prompt_template.replace("${Context}",context)
            prompt = prompt.replace("${Question}",Question)
            response = Generation.call(
                'qwen-14b-chat',
                api_key=API_KEY,
                prompt=prompt,
                seed=random.randint(1, 10000),
                result_format='message'
            )

            if response.status_code == HTTPStatus.OK:
                #print(response)
                # 获取 content 的值
                content_value = response['output']['choices'][0]['message']['content']
                print("AI输出：" + content_value)

                data = json.loads(content_value)

                Rewrite = data['Rewrite']
                Response = data['Response']

                context = (context
                           + "Question: " + Question + "\n"
                           + "Rewrite: " + Rewrite + "\n"
                           + "Response: " + Response + "\n")

                print("context：" + context)
            else:
                print('请求ID：%s，状态码：%s，错误码：%s，错误消息：%s' % (
                    response.request_id, response.status_code,
                    response.code, response.message
                ))

if __name__ == '__main__':
    call_with_messages()
