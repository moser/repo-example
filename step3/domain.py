from typing import Optional
import dataclasses as _dc


@_dc.dataclass
class User:
    id: int
    name: str
    nickname: Optional[str]
    tweets: list["Tweet"] = _dc.field(default_factory=list)


@_dc.dataclass
class Tweet:
    id: int
    text: str
    author: User
    _author_id: Optional[int] = None
