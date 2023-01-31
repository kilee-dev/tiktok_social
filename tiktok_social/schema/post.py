from dataclasses import dataclass
from typing import TypeVar
from schema.user import UserIdT

PostIdT = TypeVar('PostIdT')

@dataclass
class Post:
    id: PostIdT
    author_id: UserIdT