import json
import re
import time
import fitz
from sqlalchemy import text
from typing import Dict, List, Set, cast, Any
from fastapi import APIRouter, HTTPException

import pymupdf4llm

from app.tasks.extracting_service import run_doc_extraction
from app.dependencies.aws_client import s3_client


router = APIRouter(prefix="/sales", tags=["Sales Pipeline"], responses={
    404: {"description": "Not found"}
})

BUCKET_NAME = 'project-soat-clients'

_ZONE_VEHICLE_RE = re.compile(
    r'8\.2\s+VEH[IÍ]CULO(.+?)10\.\s+TOTAL\s+V[IÍ]CTIMAS',
    re.IGNORECASE | re.DOTALL
)
_ZONE_FACTS_RE = re.compile(
    r'S[IÍ]NTESIS\s+DE\s+LOS\s+HECHOS(.+?)13\.\s+Anexos',
    re.IGNORECASE | re.DOTALL
)
_VICTIM_BLOCK_RE = re.compile(
    r'(VICTIMA\s+\d+(?:\s+\([^)]+\))?)(.+?)(?=VICTIMA\s+\d+\b|$)',
    re.IGNORECASE | re.DOTALL
)
_FIRST_PAGE_RE = re.compile(
    r'CONDUCTORES|VEH[IÍ]CULOS\s+Y\s+PROPIETARIOS|INFORME\s+POLICIAL\s+DE\s+ACCIDENTES\s+DE\s+TR[AÁ]NSITO',
    re.IGNORECASE
)

def _normalize(text: str) -> str:
    return re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)

def get_pages_range(pages: List[Dict[str, Any]]) -> List[int]:

    matched_pages: Set[int] = set()

    for chunk in pages:
        page_number = chunk["metadata"].get("page_number")
        if page_number is not None:
            normalized_text = _normalize(chunk["text"])
            if _ZONE_VEHICLE_RE.search(normalized_text) or _ZONE_FACTS_RE.search(normalized_text) or _VICTIM_BLOCK_RE.search(normalized_text) or _FIRST_PAGE_RE.search(normalized_text):
                matched_pages.add(page_number - 1)  
    return sorted(matched_pages)


@router.post("/parse-docs", responses={500: {"description": "Database commit failed"}})
async def parse_documents(s3_prefix: str):
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(
            Bucket=BUCKET_NAME,
            Prefix=s3_prefix
        )

        result: dict = {}
        for page in page_iterator:
            if 'Contents' not in page:
                print("No files found.")
                continue

            for obj in page['Contents']:
                file_key = obj['Key']

                if file_key.endswith('/'):
                    continue

                print(f"Fetching file: {file_key}")

                response = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
                pdf_bytes = response['Body'].read()
                doc_stream = fitz.open(stream=pdf_bytes, filetype="pdf")

                pages = cast(
                    List[Dict[str, Any]],
                    pymupdf4llm.to_markdown(
                        doc=doc_stream,
                        ext="pdf",
                        page_chunks=True,
                        header=False,
                        footer=False,
                    )
                )

                pages_range = get_pages_range(pages)
                result = run_doc_extraction(doc_stream, pages_range)

        return {
            "message": "Documents parsed successfully.",
            "size": len(result.get("victim_list", [])),
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
