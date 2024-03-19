from transformers import BertTokenizer, BertForMaskedLM
import torch

# 加载BERT模型和分词器
tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
model = BertForMaskedLM.from_pretrained("bert-base-chinese")

def resolve_pronouns(context):
    # 添加特殊标记[CLS]和[SEP]
    text = "[CLS] " + context + " [SEP]"
    # 将文本转换为BERT词汇表中的标记
    tokenized_text = tokenizer.tokenize(text)
    # 寻找代词的位置
    pronoun_indices = [i for i, token in enumerate(tokenized_text) if token == "他" or token == "她" or token == "它"]
    if not pronoun_indices:
        return None

    # 用[MASK]标记替换代词
    masked_text = tokenized_text[:]
    for index in pronoun_indices:
        masked_text[index] = "[MASK]"

    # 转换为BERT的输入Tensor
    indexed_tokens = tokenizer.convert_tokens_to_ids(masked_text)
    tokens_tensor = torch.tensor([indexed_tokens])

    # 预测被遮蔽的代词
    with torch.no_grad():
        outputs = model(tokens_tensor)
        predictions = outputs[0]

    # 获取代词预测结果
    predicted_indices = [torch.argmax(prediction).item() for prediction in predictions[0][pronoun_indices]]
    predicted_tokens = tokenizer.convert_ids_to_tokens(predicted_indices)

    # 返回代词的预测结果
    resolved_pronouns = [predicted_token for predicted_token in predicted_tokens]
    return resolved_pronouns

def main():
    # 示例上下文文本
    context_text = "玛丽是一个出色的科学家。她最近发表了一篇重要的论文。"

    # 执行代词消解
    resolved_pronouns = resolve_pronouns(context_text)
    if resolved_pronouns:
        print("上下文中的代词已被消解为：", resolved_pronouns)
    else:
        print("上下文中没有找到代词。")

if __name__ == "__main__":
    main()
