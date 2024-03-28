import random
from http import HTTPStatus
import dashscope

# Set your API key here
API_KEY = 'sk-16aa6d09b6ba46699e842d5dbc89ba50'

def call_with_messages():

    prompt = """
    For an information-seeking dialog, please help reformulate the question into rewrite that can fully express the user‘s information needs without the need of context and make the rewrite result as response to answer the question. For example:

    Example #1:
    ```
        Question: 我是张三，他是李四
        Response: 我是张三，他是李四
    
        Question: 找找他的父亲的照片
        Response: 找找李四的父亲的照片
    
        Question: 去年中秋到现在的所有照片
        Response: 找找李四的父亲2023年8月15号到2024年3月28日的所有照片
    
        ...

    ```
    
    Example #2:
    ```
        Question: 我是张三，他是李四，她是刘红，他的父亲是李元芳，她的女儿是刘亦菲；
        Response: 我是张三，他是李四，她是刘红，李四的父亲是李元芳，刘红的女儿是刘亦菲；
    
        Question: 他们在一起工作，从去年中秋到现在
        Response: 张三、李四、李元芳、刘红、刘亦菲从2023年1月1号到2024年3月28日都在一起工作
    
        Question: 找找刘红女儿的参演过的电视剧
        Response: 找刘亦菲参演过的电视剧
    
        ...

    ```

    ...

    Your task (return the original content in a timely manner when the contents of the Question are completed, and the original text is not repeated):
    Context:
    ```
        Question: 老李的女儿真可爱
        Response: 老李的女儿真可爱
        Question: 他的女儿才三岁
        Response: 老李的女儿才三岁
        Question: 找找他的女儿的照片
        Response: 找找老李的女儿的照片
        ...
    ```
    
    Current Question: 从2023年中秋节到现在
    Rewrite: 现在, 你需要根据上下文**Context**并参考以上给出的示例**Example**，对当前输入**Current Question**进行重写，使得无需上下文即可充分表达用户的信息需求。The output format should always be: Rewrite: $Reason. So the question should be rewritten as: $Rewrite. Response: $Rewrite. Go ahead!
    
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
