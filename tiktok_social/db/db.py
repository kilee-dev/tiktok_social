from typing import Dict, Set, Tuple
from schema.user import UserIdT
from schema.post import PostIdT, Post
from schema.repost import RepostIdT, Repost
from schema.post_likes import PostLike
from schema.post_comments import PostComment
from schema.post_shares import PostShare
from schema.post_saves import PostSave

"""
Use in-memory DB instead of external DB to simplify code implementations
"""
class DB:
    def __init__(self):
        self.posts: Dict[PostIdT, Post] = dict()
        self.reposts: Dict[RepostIdT, Repost] = dict()
        self.post_likes: Dict[Tuple[PostIdT, UserIdT], PostLike] = dict()
        self.post_comments: Dict[Tuple[PostIdT, UserIdT], PostComment] = dict()
        self.post_shares: Dict[Tuple[PostIdT, UserIdT], PostShare] = dict()
        self.post_saves: Dict[Tuple[PostIdT, UserIdT], PostSave ] = dict()

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

    def user_like_post(self, user_id: UserIdT, post_id: PostIdT) -> None:
        self.post_likes[(post_id, user_id)] = PostLike(post_id, user_id)
        
    def user_comment_on_post(self, user_id: UserIdT, post_id: PostIdT, content: str) -> None:
        self.post_comments[(post_id, user_id)] = PostComment(post_id, user_id, content)

    def user_share_post(self, user_id:UserIdT, post_id: PostIdT) -> None:
        self.post_shares[(post_id, user_id)] = PostShare(post_id, user_id)

    def user_save_post(self, user_id: UserIdT, post_id: PostIdT) -> None:
        self.post_saves[(post_id, user_id)] = PostSave(post_id, user_id)
