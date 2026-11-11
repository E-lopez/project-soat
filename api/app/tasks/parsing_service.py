import pathlib
import re
from typing import Dict, List, cast, Any

import pymupdf4llm

from app.functions.document_utils import split_by_header_cape, split_by_header_default, split_by_header_ua

_KB_PATH = pathlib.Path(__file__).parent.parent / "data"
  

def split_by_headers(text: str, doc_name: str) -> list:
    match doc_name.lower().strip():
        case "frontier":
            return split_by_header_default(text, doc_name)
        case "united airlines":
            return split_by_header_ua(text, doc_name)
        case _:
            return split_by_header_cape(text, doc_name)


def parse_documents() -> list:
    parsed_chunks = []
    pdf_files = list(_KB_PATH.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {_KB_PATH}")
        return []

    for pdf_path in pdf_files:
        try:
            pages = cast(
              List[Dict[str, Any]], 
              pymupdf4llm.to_markdown(
                  doc=str(pdf_path),
                  page_chunks=True,
                  header=False,
                  footer=False,
              )
            )

            doc_name = pdf_path.name.split(".pdf")[0].split("_")[-1].strip()
            page_limiter = 0 if doc_name.lower() == "united airlines" else 3 
            full_text = "\n\n".join(chunk["text"] for chunk in pages if chunk["metadata"].get("page_number") > page_limiter)
            parsed_chunks.extend(split_by_headers(full_text, doc_name))

        except Exception as e:
            print(f"Error parsing {pdf_path.name}: {str(e)}")
            continue

    print(f"✅ Ingestion complete. Total parsed pages/chunks: {len(parsed_chunks)}")
    return parsed_chunks