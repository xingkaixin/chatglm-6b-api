from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    "/Users/Kevin/workspace/llm/models/chatglm-6b/", trust_remote_code=True
)
model = (
    AutoModel.from_pretrained(
        "/Users/Kevin/workspace/llm/models/chatglm-6b/", trust_remote_code=True
    )
    .half()
    .to("mps")
)

model = model.eval()
response, history = model.chat(tokenizer, "你好", history=[])
print(response)

