from abc import ABC, abstractmethod
from typing import List, DefaultDict
from collections import defaultdict
from social_graph.social_graph import SocialGraph
from user_manager.user_manager import UserIdT
from schema.post import Post, PostIdT
from db.db import DB

"""
TimelineManager manages timeline for each user. 
- There are two timelines in Tiktok.  FollowerFeedTimeline & FriendsFeedTimeline
- Given a post/repost, fanout service helps finding target audience of the author and add the post/repost to the feed post list of each user
- However, fanout service can be a bottleneck when influencers create post/repost because they have huge number of target audience
- To reduce bottleneck, run fanout service only when a post/repost author has small number of audiences
"""

class BaseTimelineManager(ABC):
    def __init__(self, db: DB, social_graph: SocialGraph):
        self.user_timelines: DefaultDict[UserIdT, List[PostIdT]] = defaultdict(list)
        self.db = db
        self.social_graph = social_graph

    def fanout_post_to_users(self, post_id: PostIdT) -> None:
        post = self.db.get_post_by_id(post_id)
        user_ids = self.fetch_fanout_audience(post.author_id)
        for user_id in user_ids:
            self.add_post_to_user_timeline(user_id, post_id)
        
    def fanout_repost_to_users(self, repost_id: PostIdT) -> None:
        repost = self.db.get_repost_by_id(repost_id)
        user_ids = self.fetch_fanout_audience(repost.repost_user_id)
        for user_id in user_ids:
            self.add_post_to_user_timeline(user_id, repost.original_post_id)

    @abstractmethod
    def fetch_fanout_audience(self, user_id: UserIdT) -> List[UserIdT]:
        pass

    def add_post_to_user_timeline(self, user_id: UserIdT, post_id: PostIdT) -> None:
        self.user_timelines[user_id].append(post_id)

    def fetch_user_timeline_posts(self, user_id: UserIdT) -> List[Post]:
        return [self.db.get_post_by_id(post_id) for post_id in self.user_timelines[user_id]]