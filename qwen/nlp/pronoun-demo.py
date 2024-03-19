import spacy

# 加载中文模型
nlp = spacy.load("zh_core_web_sm")

# 进行上下文指代消解并替换为实体名称
def resolve_pronouns(dialogue):
    resolved_dialogue = []
    preceding_entity = None
    speaker = 'A'
    for utterance in dialogue:
        doc = nlp(utterance)
        resolved_utterance = ""
        for token in doc:
            if token.pos_ == "PRON":
                # 找到代词的先行词
                for ancestor in token.ancestors:
                    if ancestor.pos_ in ["NOUN", "PROPN"]:
                        preceding_entity = ancestor.text
                        break
                if preceding_entity:
                    resolved_utterance += preceding_entity
                else:
                    resolved_utterance += token.text
            else:
                resolved_utterance += token.text
            resolved_utterance += " "
        if speaker == 'A':
            resolved_dialogue.append("A: " + resolved_utterance.strip())
            speaker = 'B'
        else:
            resolved_dialogue.append("B: " + resolved_utterance.strip())
            speaker = 'A'
    return resolved_dialogue

def main():
    # 对话文本
    dialogue = [
        "张三去了哪里？",
        "他去买菜了。",
        "他要买什么？",
        "他要买西红柿、黄瓜和土豆。"
    ]

    # 解决代词指代并替换为实体名称
    resolved_dialogue = resolve_pronouns(dialogue)

    # 打印结果
    for utterance in resolved_dialogue:
        print(utterance)

if __name__ == "__main__":
    main()
