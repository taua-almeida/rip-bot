from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class HorizonBossModel(BaseModel):
    id: Optional[int] = None
    image: Optional[str] = None
    name: str
    is_born: bool
    born_at: Optional[datetime] = None
    checked_at: datetime
    details: Optional[str] = None
    meta: str


class HorizonOtModel(BaseModel):
    id: Optional[int] = None
    author_id: int
    guild_id: Optional[int] = None
    channel_id: Optional[int] = None
    command: str
    active: bool
