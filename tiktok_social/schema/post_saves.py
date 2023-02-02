from dataclasses import dataclass
from .post import PostIdT
from .user import UserIdT

@dataclass
class PostSave:
    post_id: PostIdT
    save_user_id: UserIdT