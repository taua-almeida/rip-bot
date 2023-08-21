from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class HorizonBoss:
    image: Optional[str]
    name: str
    is_born: bool
    born_at: Optional[datetime]
    details: str
    meta: str
