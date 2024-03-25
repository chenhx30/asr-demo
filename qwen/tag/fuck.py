import requests
import spacy

# 加载spaCy的中文模型
nlp = spacy.load("zh_core_web_sm")

a = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    },

    {
        "role": "user",
        "content": "张三去了哪里？他去买菜了。他要买什么？他要买西红柿、黄瓜和土豆。"
    },
    {
        "role": "assistant",
        "content": """
                   jflsdkfajjf
                   """,


        "content2": ""
    }
]

def generate_dialogue(prompt):
    # 使用阿里巴巴的dashscope技术生成对话
    response = requests.post(
        'https://big-brother-14b-chat.gz.bcebos.com/qwen-chat',
        json={'context': prompt}
    )
    generated_dialogue = response.json().get('results', [''])[0]
    return generated_dialogue

def coreference_resolution(dialogue):
    # 将生成的对话进行解析，并进行指代消解
    doc = nlp(dialogue)
    resolved_dialogue = []
    for token in doc:
        if token.pos_ == "PRON":
            # 如果是代词，则尝试找到它所指代的实体
            resolved_token = token.text
            if token.dep_ == "nsubj" or token.dep_ == "nsubjpass":
                # 如果是主语或被动语态的主语，则使用其 head token 作为指代物
                resolved_token = token.head.text
            elif token.dep_ == "pobj" or token.dep_ == "dobj" or token.dep_ == "attr":
                # 如果是宾语、间接宾语或属性，则使用其 head token 作为指代物
                resolved_token = token.head.text
            elif token.dep_ == "poss":
                # 如果是物主代词，则使用其 head token 作为指代物
                resolved_token = token.head.text
            elif token.dep_ == "pcomp":
                # 如果是介词短语的补语，则使用其 head token 作为指代物
                resolved_token = token.head.text
            elif token.dep_ == "relcl":
                # 如果是关系从句的主语，则使用其 head token 作为指代物
                resolved_token = token.head.text
            elif token.dep_ == "nsubjpass":
                # 如果是被动语态的主语，则使用其 head token 作为指代物
                resolved_token = token.head.text
            resolved_dialogue.append(resolved_token)
        else:
            resolved_dialogue.append(token.text)
    return " ".join(resolved_dialogue)

def main():
    # 用户提问
    prompt = "谁是中国的首都？\n北京是中国的首都。\n它有多少人口？\n"

    # 生成对话
    generated_dialogue = generate_dialogue(prompt)

    # 进行指代消解
    resolved_dialogue = coreference_resolution(generated_dialogue)

    # 输出结果
    print("生成的对话：")
    print(generated_dialogue)
    print("\n进行指代消解后的对话：")
    print(resolved_dialogue)

if __name__ == "__main__":
    main()
