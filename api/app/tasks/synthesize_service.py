import json
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException
from typing import Any, Generator


from app.schemas.Dto.UsageStats import UsageStats
from app.constants.llm_models import SYNTHESIS_MODEL_ID
from app.constants.prompts import SYSTEM_SYNTHESIS_TEMPLATE
from app.dependencies.aws_client import bedrock_client


def synthesize_answer(question: str, context: str, definitions: str, stats: UsageStats) -> Generator[Any, Any, Any]:
    system_instruction = SYSTEM_SYNTHESIS_TEMPLATE.format(context=context, definitions=definitions)

    print((f"System Instruction Length: {len(system_instruction)} characters\n"))
    
    try:
        response = bedrock_client.invoke_model_with_response_stream(
            model_id=SYNTHESIS_MODEL_ID,
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "system": system_instruction,
                "messages": [
                    {
                        "role": "user",
                        "content": f"Question: {question}"
                    }
                ],
            }),
            trace_context=stats,
            contentType="application/json",
            accept="application/json",
        )
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=502, detail="Upstream model call failed.") from e
    for event in response["body"]:
        chunk = event.get("chunk")
        if chunk:
            data = json.loads(chunk["bytes"].decode("utf-8"))
            if data.get("type") == "content_block_delta":
                text_chunk = data.get("delta", {}).get("text", "")
                
                # YIELD the text chunk to the caller/frontend
                yield text_chunk
    