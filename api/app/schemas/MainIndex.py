from typing import List, Optional
from pgvector.sqlalchemy import Vector
from sqlmodel import JSON, Column, Field, SQLModel, Index

class MainIndex(SQLModel, table=True):
    __tablename__ = "main_index" # type: ignore[assignment]
    __table_args__ = (
        Index("idx_main_company_index", "company", "index"),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Metadata fields
    company: str = Field(nullable=False)
    section: Optional[str] = Field(default=None)
    index: str = Field(nullable=False)
    raw_string: str = Field(nullable=False)
    definitions: List[str] = Field(sa_column=Column(JSON), default=[])
    embedding: List[float] = Field(sa_column=Column(Vector(512)))