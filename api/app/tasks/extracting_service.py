import base64
import json
import logging
import re

import fitz
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException

from app.constants.llm_models import DOCUMENT_EXTRACTION_MODEL_ID
from app.constants.prompts import DOCUMENT_EXTRACTION_PROMPT
from app.dependencies.aws_client import bedrock_client

logger = logging.getLogger(__name__)


def run_doc_extraction(doc: fitz.Document, pages_range: list[int]) -> dict:

    image_blocks = []
    for page_num in pages_range:
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
        jpeg_bytes = pix.tobytes("jpeg")
        image_blocks.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": base64.b64encode(jpeg_bytes).decode("utf-8"),
            },
        })

    doc.close()

    image_blocks.append({"type": "text", "text": "Extract the document data as instructed."})

    try:
        print(f"Invoking Bedrock model {DOCUMENT_EXTRACTION_MODEL_ID} for document extraction...")
        response = bedrock_client.invoke_model(
            model_id=DOCUMENT_EXTRACTION_MODEL_ID,
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,
                "system": DOCUMENT_EXTRACTION_PROMPT,
                "messages": [{"role": "user", "content": image_blocks}],
            }),
            contentType="application/json",
            accept="application/json",
        )
    except (BotoCoreError, ClientError) as e:
        print(f"Error occurred while invoking Bedrock model: {str(e)}")
        logger.error("Bedrock extraction call failed: %s", str(e))
        raise HTTPException(status_code=502, detail="Upstream model call failed.") from e

    print(f"Bedrock model {DOCUMENT_EXTRACTION_MODEL_ID} invocation completed.")
    raw_text = response.get("content", [{}])[0].get("text", "").strip()
    if not raw_text:
        logger.error("Bedrock returned empty content for extraction.")
        raise HTTPException(status_code=502, detail="Model returned empty response.")

    # Strip markdown code fences Claude sometimes wraps around JSON
    clean = re.sub(r"^```(?:json)?\s*", "", raw_text, flags=re.MULTILINE).strip()
    clean = re.sub(r"```\s*$", "", clean, flags=re.MULTILINE).strip()

    print(f"Bedrock Response {clean}")
    try:
        return json.loads(clean)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse model response as JSON: %s | raw: %s", str(e), raw_text[:200])
        raise HTTPException(status_code=502, detail="Model returned malformed JSON.") from e
