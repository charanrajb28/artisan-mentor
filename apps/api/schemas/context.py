from pydantic import BaseModel

class Context(BaseModel):
    content: str
    citation: str
    source_id: str # ID of the source document
