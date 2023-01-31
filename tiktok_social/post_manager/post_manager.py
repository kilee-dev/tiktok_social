"""
Whenever new post/repost is created, the post/repost is saved in DB and fanout service is called to update user_feed cache
 - Assuming that there are two types of feed: follower_feed_manager, friends_feed_manager
"""
from db.db import DB
from schema.post import Post
from schema.repost import Repost
from feed_manager.follower_timeline_manager import FollowerTimelineManager
from feed_manager.friends_timeline_manager import FriendsTimelineManager

class PostManager:
    def __init__(self, db: DB, follower_timeline_manager: FollowerTimelineManager, friends_timeline_manager: FriendsTimelineManager):
        self.db = db
        self.follower_timeline_manager = follower_timeline_manager
        self.friends_timeline_manager = friends_timeline_manager

    def create_and_fanout_post(self, post: Post) -> None:
        self.db.create_post(post)
        self.follower_timeline_manager.fanout_post_to_users(post.id)
        self.friends_timeline_manager.fanout_post_to_users(post.id)

    def create_and_fanout_repost(self, repost: Repost) -> None:
        self.db.create_repost(repost)
        self.follower_timeline_manager.fanout_repost_to_users(repost.id)
        self.friends_timeline_manager.fanout_repost_to_users(repost.id)

    """
    TODO: like_post, comment_on_the_post, save_post
    Use counter to cache number of likes/comments/saves of each post

    TODO: Give weights between users whenever there are interactions(likes/posts) between users

    TODO: Asynchronously add fanout job to the task queue instead of waiting the job to finish

    TODO: Racing condition from put & get.
    """