import unittest
from social_graph.social_graph import SocialGraph
from .follower_timeline_manager import FollowerTimelineManager
from db.db import DB
from schema.post import Post
from schema.repost import Repost

class TestFollowerTimelineManager(unittest.TestCase):
    def test_fanout_post_to_users(self):
        db = DB()
        social_graph = SocialGraph()

        social_graph.follow_user(2, 1) # 2 -> 1
        social_graph.follow_user(3, 1) # 3 -> 1
        db.create_post(Post(1, 1)) # Post created by author_id(1)

        follower_timeline_manager = FollowerTimelineManager(db, social_graph)
        follower_timeline_manager.fanout_post_to_users(1) 

        self.assertEqual(len(follower_timeline_manager.user_timelines[1]), 0, "Should be 0")
        self.assertEqual(len(follower_timeline_manager.user_timelines[2]), 1, "Should be 1")
        self.assertEqual(len(follower_timeline_manager.user_timelines[3]), 1, "Should be 1")


    def test_fanout_repost_to_users(self):
        db = DB()
        social_graph = SocialGraph()
        follower_timeline_manager = FollowerTimelineManager(db, social_graph)

        social_graph.follow_user(2, 1) # 2 -> 1
        social_graph.follow_user(3, 2) # 3 -> 2
        social_graph.follow_user(4, 2) # 4 -> 2
        db.create_post(Post(1, 1)) # Post created by author_id(1)
        db.create_repost(Repost(1, 1, 2))
        follower_timeline_manager.fanout_repost_to_users(1) 

        self.assertEqual(len(follower_timeline_manager.user_timelines[1]), 0, "Should be 0")
        self.assertEqual(len(follower_timeline_manager.user_timelines[2]), 0, "Should be 0")
        self.assertEqual(len(follower_timeline_manager.user_timelines[3]), 1, "Should be 1")
        self.assertEqual(len(follower_timeline_manager.user_timelines[4]), 1, "Should be 1")


    def fetch_fanout_audience(self):
        db = DB()
        social_graph = SocialGraph()
        follower_timeline_manager = FollowerTimelineManager(db, social_graph)

        social_graph.follow_user(2, 1) # 2 -> 1
        social_graph.follow_user(3, 2) # 3 -> 2
        social_graph.follow_user(4, 2) # 4 -> 2

        self.assertEqual(len(follower_timeline_manager.fetch_fanout_audience(1)), 1, "Should be 1")
        self.assertEqual(len(follower_timeline_manager.fetch_fanout_audience(2)), 2, "Should be 2")
        self.assertEqual(len(follower_timeline_manager.fetch_fanout_audience(3)), 0, "Should be 0")
        self.assertEqual(len(follower_timeline_manager.fetch_fanout_audience(4)), 0, "Should be 0")

    def add_post_to_user_timeline(self):
        db = DB()
        social_graph = SocialGraph()
        follower_timeline_manager = FollowerTimelineManager(db, social_graph)

        follower_timeline_manager.add_post_to_user_timeline(1, 1)
        self.assertEqual(len(follower_timeline_manager.fetch_user_timeline_posts(1)), 1, "Should be 1")

    def fetch_user_timeline_posts(self):
        db = DB()
        social_graph = SocialGraph()
        follower_timeline_manager = FollowerTimelineManager(db, social_graph)

        follower_timeline_manager.add_post_to_user_timeline(1, 1)
        self.assertEqual(len(follower_timeline_manager.fetch_user_timeline_posts(1)), 1, "Should be 1")