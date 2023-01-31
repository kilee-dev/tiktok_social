from dataclasses import dataclass
from typing import TypeVar
from schema.user import UserIdT
from schema.post import PostIdT

RepostIdT = TypeVar('RepostIdT')

@dataclass
class Repost:
    id: RepostIdT
    original_post_id: PostIdT
    repost_user_id: UserIdT