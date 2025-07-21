from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field

class DocumentType(str, Enum):
    """Enumeration for the basic types of documents."""
    RESUME = "resume"
    CITATION = "citation"
    README = "readme"
    OTHER = "other"


class SimpleClassification(BaseModel):
    """
    Classify a document by its type
    and provide a simple description.
    """
    type: DocumentType = Field(
        ...,
        description="The classified type of the document.It can only be of 3 type resume, citation which is research paper, readme file of github or other"
    )
    
    description: str = Field(
        ...,
        description="A brief, human-readable description of the document's content or purpose."
    )

    class Config:
        """Pydantic model configuration."""
        anystr_strip_whitespace = True
        validate_assignment = True

