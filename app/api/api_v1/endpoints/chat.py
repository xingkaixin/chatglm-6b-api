import json
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sse_starlette.sse import EventSourceResponse

from app import schemas
from app.api import deps

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
async def create_chat_completions(
    *,
    tokenizer=Depends(deps.get_tokenizer),
    model=Depends(deps.get_llm_model),
    body: schemas.Request.LLMInput,
    request: Request,
):
    question = body.messages[-1]
    if question.role == "user":
        question = question.content
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No Question Found")

    history = []
    user_question = ""
    for message in body.messages:
        if message.role == "system":
            history.append((message.content, "OK"))
        if message.role == "user":
            user_question = message.content
        elif message.role == "assistant":
            assistant_answer = message.content
            history.append((user_question, assistant_answer))

    print(f"{question=} {history=}")

    if body.stream:

        async def eval_chatglm():
            sends = 0
            first = True
            for response, _ in model.stream_chat(
                tokenizer,
                question,
                history,
                temperature=body.temperature,
                top_p=body.top_p,
                max_length=max(2048, body.max_tokens),
            ):
                if await request.is_disconnected():
                    return
                ret = response[sends:]
                sends = len(response)
                if first:
                    first = False
                    # sse start
                    yield json.dumps(
                        sse_data(delta_data={"role": "assistant"}),
                        ensure_ascii=False,
                    )
                # sse response
                yield json.dumps(
                    sse_data(delta_data={"content": ret}), ensure_ascii=False
                )
            # sse stop
            yield json.dumps(
                sse_data(delta_data={}, finish_reason="stop"), ensure_ascii=False
            )
            yield "[DONE]"

        return EventSourceResponse(eval_chatglm(), ping=10000)
    else:
        response, _ = model.chat(
            tokenizer,
            question,
            history,
            temperature=body.temperature,
            top_p=body.top_p,
            max_length=body.max_tokens,
        )
        return data(response)


def data(
    response: str,
) -> schemas.Response.ChatCompletion:
    message = schemas.Response.Message(content=response)
    choice = schemas.Response.Choice(message=message)
    return schemas.Response.ChatCompletion(choices=[choice])


def sse_data(delta_data: Dict[str, str], finish_reason: str = None) -> Dict[str, Any]:
    message = schemas.Response.DeltaChoice(
        delta=delta_data, finish_reason=finish_reason
    )
    return schemas.Response.DeltaChatCompletion(choices=[message]).dict()
