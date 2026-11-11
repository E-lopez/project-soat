import json
import logging
import re

from botocore.exceptions import BotoCoreError, ClientError

from app.constants.llm_pricing import BEDROCK_PRICING
from app.constants.llm_models import JUDGE_MODEL_ID
from app.dependencies.aws_client import get_bedrock_client
from app.constants.prompts import JUDGE_PROMPT


logger = logging.getLogger(__name__)
_CODE_FENCE_RE = re.compile(r"```(?:json)?\n(.*?)\n```", re.DOTALL)


def run_rag_eval(
    user_query: str,
    retrieved_context: str,
    generated_response: str,
) -> dict:
    filled_prompt = (
        JUDGE_PROMPT
        .replace("{{USER_QUERY}}", user_query)
        .replace("{{RETRIEVED_CONTEXT}}", retrieved_context)
        .replace("{{GENERATED_RESPONSE}}", generated_response)
    )

    try:
        client = get_bedrock_client()
        response = client.invoke_model(
            modelId=JUDGE_MODEL_ID,
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2048,
                "system": filled_prompt,
                "messages": [{"role": "user", "content": "Evaluate."}],
            }),
            contentType="application/json",
            accept="application/json",
        )
        result = json.loads(response["body"].read())
        text = result["content"][0]["text"]
        match = _CODE_FENCE_RE.search(text)
        return json.loads(match.group(1) if match else text)
    except (BotoCoreError, ClientError):
        print(f"ERRORS: {BotoCoreError, ClientError}")
        logger.exception("RAG eval: Bedrock call failed — skipping eval for this transaction.")
        return {}
