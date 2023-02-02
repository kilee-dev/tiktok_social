from dataclasses import dataclass
from .post import PostIdT
from .user import UserIdT

@dataclass
class PostLike:
    post_id: PostIdT
    like_user_id: UserIdT