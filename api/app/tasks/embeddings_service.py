import json
from typing import Optional

from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException

from app.schemas.Dto.UsageStats import UsageStats
from app.constants.llm_models import EMBEDDING_MODEL_ID
from app.dependencies.aws_client import bedrock_client


def embed_text(text: str, stats: Optional[UsageStats]) -> list[float]:
    try:
        response = bedrock_client.invoke_model(
            model_id=EMBEDDING_MODEL_ID,
            body=json.dumps({
                "inputText": text,
                "dimensions": 512,
                "normalize": True
            }),
            trace_context=stats,
            contentType="application/json",
            accept="application/json",
        )
    except (BotoCoreError, ClientError) as e:
        print(f"Error invoking model { EMBEDDING_MODEL_ID }: {str(e)}")
        raise HTTPException(status_code=502, detail="Upstream model call failed.") from e
    return response["embedding"]
