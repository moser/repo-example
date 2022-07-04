from typing import Optional
import dataclasses as _dc


@_dc.dataclass
class User:
    id: int
    name: str
    nickname: Optional[str]
