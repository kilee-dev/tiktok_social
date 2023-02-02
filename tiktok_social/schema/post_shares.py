from dataclasses import dataclass
from .post import PostIdT
from .user import UserIdT

@dataclass
class PostShare:
    post_id: PostIdT
    sharing_user_id: UserIdT