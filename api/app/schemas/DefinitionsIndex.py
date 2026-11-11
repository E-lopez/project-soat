from typing import Optional
from sqlmodel import Field, SQLModel, Index

class DefinitionsIndex(SQLModel, table=True):
    __tablename__ = "definitions_index" # type: ignore[assignment]
    __table_args__ = (
        Index("idx_def_company_index", "company", "index"),
    )

    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Metadata fields
    company: str = Field(nullable=False)
    index: str = Field(nullable=False)
    key_word: str = Field(nullable=False)
    raw_string: str = Field(nullable=False)