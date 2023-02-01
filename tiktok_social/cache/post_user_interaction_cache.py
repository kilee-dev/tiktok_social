from schema.user import UserIdT
from schema.post import PostIdT
from typing import Set, Tuple

class PostUserInteractionCache:
    def __init__(self):
        self.user_like_post_cache: Set[Tuple[UserIdT, PostIdT]] = set()
        self.user_save_post_cache: Set[Tuple[UserIdT, PostIdT]] = set()

    def put_user_like_post(self, user_id: UserIdT, post_id:PostIdT):
        self.user_like_post_cache.add((user_id, post_id))

    def get_user_like_post(self, user_id: UserIdT, post_id:PostIdT) -> bool:
        return (user_id, post_id) in self.user_like_post_cache

    def put_user_save_post(self, user_id: UserIdT, post_id: PostIdT):
        self.user_save_post_cache.add((user_id, post_id))

    def get_user_save_post(self, user_id: UserIdT, post_id:PostIdT) -> bool:
        return (user_id, post_id) in self.user_save_post_cache