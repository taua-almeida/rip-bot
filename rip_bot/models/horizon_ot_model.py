from typing import Optional
from pydantic import BaseModel


class HorizonOtModel(BaseModel):
    id: Optional[int] = None
    author_id: int
    guild_id: Optional[int] = None
    channel_id: Optional[int] = None
    command: str
    active: bool
