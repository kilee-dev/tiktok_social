"""
Whenever new post/repost is created, the post/repost is saved in DB and fanout service is called to update user_feed cache
 - Assuming that there are two types of feed: follower_feed_manager, friends_feed_manager
"""
from cache.post_counter_cache import PostCounterCache
from cache.post_user_interaction_cache import PostUserInteractionCache
from db.db import DB
from schema.user import UserIdT
from schema.post import Post, PostIdT
from schema.repost import Repost
from feed_manager.follower_timeline_manager import FollowerTimelineManager
from feed_manager.friends_timeline_manager import FriendsTimelineManager
from social_graph.social_graph import SocialGraph

class PostManager:
    def __init__(self, 
                db: DB, 
                follower_timeline_manager: FollowerTimelineManager, 
                friends_timeline_manager: FriendsTimelineManager, 
                post_counter_cache: PostCounterCache,
                post_user_interaction_cache: PostUserInteractionCache,
                social_graph: SocialGraph
        ):
        self.db = db
        self.follower_timeline_manager = follower_timeline_manager
        self.friends_timeline_manager = friends_timeline_manager
        self.post_counter_cache = post_counter_cache
        self.post_user_interaction_cache = post_user_interaction_cache
        self.social_graph = social_graph

    def create_and_fanout_post(self, post: Post) -> None:
        self.db.create_post(post)
        self.follower_timeline_manager.fanout_post_to_users(post.id)
        self.friends_timeline_manager.fanout_post_to_users(post.id)

    def create_and_fanout_repost(self, repost: Repost) -> None:
        self.db.create_repost(repost)
        self.follower_timeline_manager.fanout_repost_to_users(repost.id)
        self.friends_timeline_manager.fanout_repost_to_users(repost.id)

    def user_like_post(self, user_id: UserIdT, post_id: PostIdT) -> None:
        self.db.user_like_post(user_id, post_id)
        self.post_counter_cache.increment_post_likes_counts(post_id)
        self.post_user_interaction_cache.put_user_like_post(user_id, post_id)

        # increment weights between user and author of post by 1
        post = self.db.get_post_by_id(post_id)
        self.social_graph.increment_weight(user_id, post.author_id, 1)

    def user_comment_on_post(self, user_id: UserIdT, post_id: PostIdT, content: str) -> None:
        self.db.user_comment_on_post(user_id, post_id, content)
        self.post_counter_cache.increment_post_comments_counts(post_id)

        # increment weights between user and author of post by 1
        post = self.db.get_post_by_id(post_id)
        self.social_graph.increment_weight(user_id, post.author_id, 1)

    def user_save_post(self, user_id: UserIdT, post_id: PostIdT):
        self.db.user_save_post(user_id, post_id)
        self.post_counter_cache.increment_post_saves_counts(post_id)
        self.post_user_interaction_cache.put_user_save_post(user_id, post_id)

        # increment weights between user and author of post by 1
        post = self.db.get_post_by_id(post_id)
        self.social_graph.increment_weight(user_id, post.author_id, 1)

    def user_share_post(self, user_id: UserIdT, post_id:PostIdT) -> None:
        self.db.user_share_post(user_id, post_id)
        self.post_counter_cache.increment_post_shares_counts(post_id)
        
        # increment weights between user and author of post by 1
        post = self.db.get_post_by_id(post_id)
        self.social_graph.increment_weight(user_id, post.author_id, 1)

    """
    TODO: Asynchronously add fanout job to the task queue instead of waiting the job to finish

    TODO: Racing condition from put & get.
    """