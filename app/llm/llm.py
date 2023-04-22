import platform

import torch
from text2vec import SentenceModel
from transformers import AutoModel, AutoTokenizer

os_type = platform.system()
has_cuda = torch.cuda.is_available()


def init_llm(model_path: str):
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    if os_type == "Darwin" and not has_cuda:
        model = (
            AutoModel.from_pretrained(model_path, trust_remote_code=True)
            .half()
            .to("mps")
        )
    elif has_cuda:
        model = (
            AutoModel.from_pretrained(model_path, trust_remote_code=True).half().cuda()
        )
    else:
        model = AutoModel.from_pretrained(model_path, trust_remote_code=True).float()
    model = model.eval()
    return tokenizer, model


def init_embeddings(model_path: str):
    model = SentenceModel(model_path)
    return model
