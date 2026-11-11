import json
from typing import Optional

from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException

from app.constants.prompts import DEFINITIONS_CALSSIFICATION_PROMPT
from app.schemas.Dto.UsageStats import UsageStats
from app.constants.llm_models import EMBEDDING_MODEL_ID, GUARDRAIL_PROHIBITED_MODEL_ID
from app.dependencies.aws_client import bedrock_client, get_bedrock_client

PROMPT_TEMPLATE = (
    "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
    "{system_prompt}"
    "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
    "{input_text}"
    "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
    "{definitions}"
    "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
)


def classify_definitions(text: str, defs: str) -> list[str]:
    client = get_bedrock_client()
    
    prompt = PROMPT_TEMPLATE.format(
        system_prompt=DEFINITIONS_CALSSIFICATION_PROMPT,
        input_text=text,
        definitions=defs,
    )

    try:
        response = client.invoke_model(
            modelId=GUARDRAIL_PROHIBITED_MODEL_ID,
            body=json.dumps({"prompt": prompt, "max_gen_len": 500, "temperature": 0.0}),
            contentType="application/json",
            accept="application/json",
        )
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=502, detail="Upstream model call failed.") from e

    result = json.loads(response["body"].read())

    return result.get("generation", "[]").strip()

