from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class Usage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class Message(BaseModel):
    role: str = "assistant"
    content: str


class Choice(BaseModel):
    index: int = 0
    message: Message
    finish_reason: str = "stop"


class ChatCompletion(BaseModel):
    """
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

    """

    id: str = "chatcmpl-123"
    object: str = "chat.completion"
    created: int = int(datetime.now().timestamp())
    choices: List[Choice]
    usage: Usage = Usage()


class DeltaChoice(BaseModel):
    delta: Dict[str, str]
    index: int = 0
    finish_reason: Optional[str]


class DeltaChatCompletion(BaseModel):
    """
    {
      "id": "chatcmpl-123",
      "object": "chat.completion.chunk",
      "created": 1682173800,
      "model": "gpt-3.5-turbo-0301",
      "choices": [
        {
          "delta": {
            "role": "assistant"
          },
          "index": 0,
          "finish_reason": null
        }
      ]
    }

    {
      "id": "chatcmpl-123",
      "object": "chat.completion.chunk",
      "created": 1682173800,
      "model": "gpt-3.5-turbo-0301",
      "choices": [
        {
          "delta": {
            "content": "城"
          },
          "index": 0,
          "finish_reason": null
        }
      ]
    }

    {
      "id": "chatcmpl-123",
      "object": "chat.completion.chunk",
      "created": 1682173800,
      "model": "gpt-3.5-turbo-0301",
      "choices": [
        {
          "delta": {},
          "index": 0,
          "finish_reason": "stop"
        }
      ]
    }

    data: [DONE]
    """

    id: str = "chatcmpl-123"
    object: str = "chat.completion.chunk"
    created: int = int(datetime.now().timestamp())
    model: str = "gpt-3.5-turbo-0301"
    choices: List[DeltaChoice]
