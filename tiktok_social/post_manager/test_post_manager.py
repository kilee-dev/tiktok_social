import unittest
from social_graph.social_graph import SocialGraph
from feed_manager.follower_timeline_manager import FollowerTimelineManager
from feed_manager.friends_timeline_manager import FriendsTimelineManager
from db.db import DB
from .post_manager import PostManager
from schema.post import Post
from schema.repost import Repost

class TestPostManager(unittest.TestCase):
    def test_create_and_fanout_post(self):
        db = DB()
        social_graph = SocialGraph()
        follower_timeline_manager = FollowerTimelineManager(db, social_graph)
        friends_timeline_manager = FriendsTimelineManager(db, social_graph)
        post_manager = PostManager(db, follower_timeline_manager, friends_timeline_manager)
        
        social_graph.follow_user(2, 1)
        social_graph.follow_user(2, 3)
        social_graph.follow_user(3, 2)
        social_graph.follow_user(4, 1)

        post_manager.create_and_fanout_post(Post(1, 1))
        post_manager.create_and_fanout_post(Post(2, 2))
        
        self.assertEqual(len(follower_timeline_manager.fetch_user_timeline_posts(1)), 0, "Should be 0")
        self.assertEqual(len(follower_timeline_manager.fetch_user_timeline_posts(2)), 1, "Should be 1")
        self.assertEqual(len(follower_timeline_manager.fetch_user_timeline_posts(3)), 1, "Should be 1")
        self.assertEqual(len(follower_timeline_manager.fetch_user_timeline_posts(4)), 1, "Should be 1")

        self.assertEqual(len(friends_timeline_manager.fetch_user_timeline_posts(1)), 0, "Should be 0")
        self.assertEqual(len(friends_timeline_manager.fetch_user_timeline_posts(2)), 0, "Should be 0")
        self.assertEqual(len(friends_timeline_manager.fetch_user_timeline_posts(3)), 1, "Should be 1")
        self.assertEqual(len(friends_timeline_manager.fetch_user_timeline_posts(4)), 0, "Should be 0")


    def test_create_and_fanout_repost(self):
        db = DB()
        social_graph = SocialGraph()
        follower_timeline_manager = FollowerTimelineManager(db, social_graph)
        friends_timeline_manager = FriendsTimelineManager(db, social_graph)
        post_manager = PostManager(db, follower_timeline_manager, friends_timeline_manager)
        
        db.create_post(Post(1, 2))

        social_graph.follow_user(2, 1)
        social_graph.follow_user(2, 3)
        social_graph.follow_user(3, 2)
        social_graph.follow_user(4, 1)
        social_graph.follow_user(1, 4)

        post_manager.create_and_fanout_repost(Repost(1, 1, 1))
        
        self.assertEqual(len(follower_timeline_manager.fetch_user_timeline_posts(1)), 0, "Should be 0")
        self.assertEqual(len(follower_timeline_manager.fetch_user_timeline_posts(2)), 1, "Should be 1")
        self.assertEqual(len(follower_timeline_manager.fetch_user_timeline_posts(3)), 0, "Should be 0")
        self.assertEqual(len(follower_timeline_manager.fetch_user_timeline_posts(4)), 1, "Should be 1")

        self.assertEqual(len(friends_timeline_manager.fetch_user_timeline_posts(1)), 0, "Should be 0")
        self.assertEqual(len(friends_timeline_manager.fetch_user_timeline_posts(2)), 0, "Should be 0")
        self.assertEqual(len(friends_timeline_manager.fetch_user_timeline_posts(3)), 0, "Should be 0")
        self.assertEqual(len(friends_timeline_manager.fetch_user_timeline_posts(4)), 1, "Should be 1")