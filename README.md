# ChatGLM-6B API

## chatbot-ui to chat.
[chatbot-ui](https://github.com/mckaywrigley/chatbot-ui)
![chat](https://raw.githubusercontent.com/xingkaixin/chatglm-6b-api/main/doc/chat.png)
## CPU&GPU
![cpu](https://raw.githubusercontent.com/xingkaixin/chatglm-6b-api/main/doc/cpu.png)
![gpu](https://raw.githubusercontent.com/xingkaixin/chatglm-6b-api/main/doc/gpu.png)

## download model
1.llm
```bash
git clone https://huggingface.co/THUDM/chatglm-6b-int4
```
2. text2vec
```bash
git clone https://huggingface.co/GanymedeNil/text2vec-large-chinese
```

## run prod server
Running on port 6006, for the convenience of deployment on [audodl](https://www.autodl.com/).
```bash
gunicorn -c gunicorn.conf.py main:app
```




## 实现的接口
### List models
`GET /v1/models`

*Example request*
```
curl https://127.0.0.1:8000/v1/models \
  -H "Authorization: Bearer $API_KEY"
```

*Response*
```
{
  "data": [
    {
      "id": "model-id-0",
      "object": "model",
      "owned_by": "organization-owner",
      "permission": [...]
    },
    {
      "id": "model-id-1",
      "object": "model",
      "owned_by": "organization-owner",
      "permission": [...]
    },
    {
      "id": "model-id-2",
      "object": "model",
      "owned_by": "openai",
      "permission": [...]
    },
  ],
  "object": "list"
}
```

### Create Chat Completion
`POST /v1/chat/completions`
*Example request*
```
curl https://127.0.0.1:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'

```
*Parameters*
```
{
  "model": "gpt-3.5-turbo",
  "messages": [{"role": "user", "content": "Hello!"}]
}
```
*Response*
```
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "\n\nHello there, how may I assist you today?",
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}
```

### Create embeddings
`POST /v1/embeddings`

*Example request*
```
curl https://127.0.0.1:8000/v1/embeddings \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "The food was delicious and the waiter...",
    "model": "text-embedding-ada-002"
  }'
```
*Parameters*
```
{
  "model": "text-embedding-ada-002",
  "input": "The food was delicious and the waiter..."
}
```
*Response*
```
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [
        0.0023064255,
        -0.009327292,
        .... (1536 floats total for ada-002)
        -0.0028842222,
      ],
      "index": 0
    }
  ],
  "model": "text-embedding-ada-002",
  "usage": {
    "prompt_tokens": 8,
    "total_tokens": 8
  }
}
```



## create conda env
```bash
conda create -n llm_py38 python=3.8
conda activate llm_py38
```

## poetry env
```bash
pip install poetry
poetry config virtualenvs.create false
```


## arm macos torch
[Accelerated PyTorch training on Mac](https://developer.apple.com/metal/pytorch/)

```bash
conda install pytorch torchvision torchaudio -c pytorch-nightly
```

check if torch is installed
```python
import torch
if torch.backends.mps.is_available():
    mps_device = torch.device("mps")
    x = torch.ones(1, device=mps_device)
    print (x)
else:
    print ("MPS device not found.")
```

output
```
tensor([1.], device='mps:0')
```

## fix charset-normalizer error
```
pip install --force-reinstall charset-normalizer==3.1.0
```


## poe install
```bash
poetry install
```


## dev start server
```bash
uvicorn main:app --reload
```

## test streaming response
```bash
echo '{
  "model": "gpt-3.5-turbo",
  "messages": [
    {"role": "system", "content": "你是一个上海旅游专家"},
    {"role": "user", "content": "上海哪里好玩"},
    {"role": "assistant", "content": "城隍庙不错"},
    {"role": "user", "content": "那里是玩什么的"}
  ],
  "stream": true
}' | http -S POST http://localhost:8000/v1/chat/completions/
```




