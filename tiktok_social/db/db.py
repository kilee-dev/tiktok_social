from typing import Dict
from schema.post import PostIdT, Post
from schema.repost import RepostIdT, Repost

"""
Use in-memory DB instead of external DB to simplify code implementations
"""
class DB:
    def __init__(self):
        self.posts: Dict[PostIdT, Post] = dict()
        self.reposts: Dict[RepostIdT, Repost] = dict()

    def create_post(self, post: Post) -> None:
        self.posts[post.id] = post
        
    def get_post_by_id(self, post_id: PostIdT) -> Post:
        # NOTE: assume that only valid input comes in to simplify code logics
        return self.posts[post_id]

    def create_repost(self, repost: Repost) -> None:
        self.reposts[repost.id] = repost

    def get_repost_by_id(self, repost_id: RepostIdT) -> RepostIdT:
        # NOTE: assume that only valid input comes in to simplify code logics
        return self.reposts[repost_id]