import unittest
from social_graph.social_graph import SocialGraph
from feed_manager.follower_timeline_manager import FollowerTimelineManager
from feed_manager.friends_timeline_manager import FriendsTimelineManager
from cache.post_counter_cache import PostCounterCache
from cache.post_user_interaction_cache import PostUserInteractionCache
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
        post_counter_cache = PostCounterCache()
        post_user_interaction_cache = PostUserInteractionCache()
        post_manager = PostManager(
            db, 
            follower_timeline_manager, 
            friends_timeline_manager,
            post_counter_cache,
            post_user_interaction_cache,
            social_graph
        )
        
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
        post_counter_cache = PostCounterCache()
        post_user_interaction_cache = PostUserInteractionCache()
        post_manager = PostManager(
            db, 
            follower_timeline_manager, 
            friends_timeline_manager,
            post_counter_cache,
            post_user_interaction_cache,
            social_graph
        )
        
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

    def test_user_like_post(self):
        db = DB()
        social_graph = SocialGraph()
        follower_timeline_manager = FollowerTimelineManager(db, social_graph)
        friends_timeline_manager = FriendsTimelineManager(db, social_graph)
        post_counter_cache = PostCounterCache()
        post_user_interaction_cache = PostUserInteractionCache()
        post_manager = PostManager(
            db, 
            follower_timeline_manager, 
            friends_timeline_manager,
            post_counter_cache,
            post_user_interaction_cache,
            social_graph
        )

        social_graph.follow_user(1, 2) # 1 -> 2
        social_graph.follow_user(2, 1) # 1 -> 2
        social_graph.follow_user(1, 3) # 1 -> 3
        social_graph.follow_user(3, 1) # 3 -> 1
        db.create_post(Post(1, 1)) # User 1 created Post 1
        
        post_manager.user_like_post(2, 1) # User 2 liked Post 1
        post_manager.user_like_post(3, 1) # User 3 liked Post 1

        self.assertEqual(post_counter_cache.post_likes_counts[1], 2, "Should be 2")
        self.assertEqual((2,1) in post_user_interaction_cache.user_like_post_cache, True, "Should be true")
        self.assertEqual((3,1) in post_user_interaction_cache.user_like_post_cache, True, "Should be true")
        self.assertEqual((1,1) in post_user_interaction_cache.user_like_post_cache, False, "Should be true")
        self.assertEqual(social_graph.follower_relationship[2][1], 1, "Should be 1")
        self.assertEqual(social_graph.follower_relationship[3][1], 1, "Should be 1")
    
    
    def test_user_comment_on_post(self):
        db = DB()
        social_graph = SocialGraph()
        follower_timeline_manager = FollowerTimelineManager(db, social_graph)
        friends_timeline_manager = FriendsTimelineManager(db, social_graph)
        post_counter_cache = PostCounterCache()
        post_user_interaction_cache = PostUserInteractionCache()
        post_manager = PostManager(
            db, 
            follower_timeline_manager, 
            friends_timeline_manager,
            post_counter_cache,
            post_user_interaction_cache,
            social_graph
        )

        social_graph.follow_user(1, 2) # 1 -> 2
        social_graph.follow_user(2, 1) # 1 -> 2
        social_graph.follow_user(1, 3) # 1 -> 3
        social_graph.follow_user(3, 1) # 3 -> 1
        db.create_post(Post(1, 1)) # User 1 created Post 1
        
        post_manager.user_comment_on_post(2, 1, "Cool") # User 2 liked Post 1
        post_manager.user_comment_on_post(3, 1, "Lmaooo") # User 3 liked Post 1

        self.assertEqual(post_counter_cache.post_comments_counts[1], 2, "Should be 2")
        self.assertEqual(social_graph.follower_relationship[2][1], 1, "Should be 1")
        self.assertEqual(social_graph.follower_relationship[3][1], 1, "Should be 1")
    

    def test_user_save_post(self):
        db = DB()
        social_graph = SocialGraph()
        follower_timeline_manager = FollowerTimelineManager(db, social_graph)
        friends_timeline_manager = FriendsTimelineManager(db, social_graph)
        post_counter_cache = PostCounterCache()
        post_user_interaction_cache = PostUserInteractionCache()
        post_manager = PostManager(
            db, 
            follower_timeline_manager, 
            friends_timeline_manager,
            post_counter_cache,
            post_user_interaction_cache,
            social_graph
        )

        social_graph.follow_user(1, 2) # 1 -> 2
        social_graph.follow_user(2, 1) # 1 -> 2
        social_graph.follow_user(1, 3) # 1 -> 3
        social_graph.follow_user(3, 1) # 3 -> 1
        db.create_post(Post(1, 1)) # User 1 created Post 1
        
        post_manager.user_save_post(2, 1) # User 2 liked Post 1
        post_manager.user_save_post(3, 1) # User 3 liked Post 1

        self.assertEqual(post_counter_cache.post_saves_counts[1], 2, "Should be 2")
        self.assertEqual(social_graph.follower_relationship[2][1], 1, "Should be 1")
        self.assertEqual(social_graph.follower_relationship[3][1], 1, "Should be 1")
    


    def test_user_share_post(self):
        db = DB()
        social_graph = SocialGraph()
        follower_timeline_manager = FollowerTimelineManager(db, social_graph)
        friends_timeline_manager = FriendsTimelineManager(db, social_graph)
        post_counter_cache = PostCounterCache()
        post_user_interaction_cache = PostUserInteractionCache()
        post_manager = PostManager(
            db, 
            follower_timeline_manager, 
            friends_timeline_manager,
            post_counter_cache,
            post_user_interaction_cache,
            social_graph
        )

        social_graph.follow_user(1, 2) # 1 -> 2
        social_graph.follow_user(2, 1) # 1 -> 2
        social_graph.follow_user(1, 3) # 1 -> 3
        social_graph.follow_user(3, 1) # 3 -> 1
        db.create_post(Post(1, 1)) # User 1 created Post 1
        
        post_manager.user_share_post(2, 1) # User 2 liked Post 1
        post_manager.user_share_post(3, 1) # User 3 liked Post 1

        self.assertEqual(post_counter_cache.post_shares_counts[1], 2, "Should be 2")
        self.assertEqual(social_graph.follower_relationship[2][1], 1, "Should be 1")
        self.assertEqual(social_graph.follower_relationship[3][1], 1, "Should be 1")