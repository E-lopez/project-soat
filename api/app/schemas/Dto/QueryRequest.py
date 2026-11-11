import re
from pydantic import BaseModel, field_validator

_CONTROL_RE = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')

class QueryRequest(BaseModel):
    query: str
    company: str

    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        v = _CONTROL_RE.sub('', v).strip()
        if not v:
            raise ValueError('Query must not be empty.')
        if len(v) > 500:
            raise ValueError('Query must not exceed 500 characters.')
        return v