from typing import Optional
from pydantic import BaseModel


class RequestModel(BaseModel):
    max_pages: Optional[int] = 1
    proxy: Optional[str] = None
