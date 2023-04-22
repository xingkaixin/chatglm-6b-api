from app.core.config import embedding_model, llm_model
from app.llm import init_embeddings, init_llm

tokenizer, model = init_llm(llm_model)
embeddings_model = init_embeddings(embedding_model)


def get_tokenizer():
    return tokenizer


def get_llm_model():
    return model


def get_embeddings_model():
    return embeddings_model
