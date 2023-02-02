from dataclasses import dataclass
from .post import PostIdT
from .user import UserIdT

@dataclass
class PostComment:
    post_id: PostIdT
    comment_user_id: UserIdT
    content: str