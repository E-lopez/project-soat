import re
import json
import logging

from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException

from app.constants.llm_models import GUARDRAIL_PROHIBITED_MODEL_ID
from app.constants.prompts import GUARDRAIL_PROHIBITED_PROMPT
from app.dependencies.aws_client import get_bedrock_client


logger = logging.getLogger(__name__)

_INJECTION_RE = re.compile(
    r'(ignore (previous|above|all)|system\s*:|you are now|disregard|<\|\w|\[\[|]]|forget (your|all)|new (role|persona)|act as (a|an)\b)',
    re.IGNORECASE
)
PROMPT_TEMPLATE = (
    "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
    "{system_prompt}"
    "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
    "{query}"
    "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
)

def run_query_guardrails(query: str) -> bool:
    if _INJECTION_RE.search(query):
        logger.warning("Injection pattern detected: %s", query)
        return False

    client = get_bedrock_client()

    prompt = PROMPT_TEMPLATE.format(
        system_prompt=GUARDRAIL_PROHIBITED_PROMPT,
        query=query,
    )

    try:
        response = client.invoke_model(
            modelId=GUARDRAIL_PROHIBITED_MODEL_ID,
            body=json.dumps({"prompt": prompt, "max_gen_len": 10, "temperature": 0.0}),
            contentType="application/json",
            accept="application/json",
        )
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=502, detail="Upstream model call failed.") from e

    result = json.loads(response["body"].read())
    verdict = result.get("generation", "PROHIBITED").strip().upper()

    logger.info("Guardrail verdict: %s", verdict)

    return verdict == "ALLOWED"
