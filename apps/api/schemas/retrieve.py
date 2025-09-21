from pydantic import BaseModel
from typing import Optional, Dict

class RetrieveRequest(BaseModel):
    query: str
    filters: Optional[Dict[str, str]] = None
    k: int = 10
