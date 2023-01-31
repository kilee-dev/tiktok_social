from feed_manager.base import BaseTimelineManager
from typing import List
from user_manager.user_manager import UserIdT
from db.db import DB
from social_graph.social_graph import SocialGraph

class FriendsTimelineManager(BaseTimelineManager):
    def __init__(self, db: DB, social_graph: SocialGraph):
        super().__init__(db, social_graph)

    def fetch_fanout_audience(self, user_id:UserIdT) -> List[UserIdT]:
        return self.social_graph.get_friends_by_user_id(user_id)
