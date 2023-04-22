from typing import List

from pydantic import BaseModel, Field


class Usage(BaseModel):
    prompt_tokens: int = 0
    total_tokens: int = 0


class EmbeddingData(BaseModel):
    object: str = "embedding"
    embedding: List[float]
    index: int = 0


class Embeddings(BaseModel):
    """
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
    """

    object: str = "list"
    data: List[EmbeddingData]
    model: str = "text-embedding-ada-002"
    usage: Usage = Field(default_factory=lambda: Usage())
