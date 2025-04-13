from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    file_id: str
    chunk_size: Optional[int] = 100 # cut from character # 1 to 100
    overlap_size: Optional[int] = 20 # cut from character # 80 to 180, to avoid any cut for necessary words/idea
    do_reset: Optional[int] = 0 # 0: no reset, 1: reset, to previous chunks
