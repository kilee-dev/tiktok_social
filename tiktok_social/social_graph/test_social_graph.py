from .social_graph import SocialGraph
import unittest

class TestSocialGraph(unittest.TestCase):
    def test_recommend_mutual_friends(self):
        # A -> B -> C : Recommending C
        # A -> B <- C : Recommeding C
        # A <-> B <- C: Recommending C's
        test_social_graph = SocialGraph()
        test_social_graph.follow_user(1, 2)
        test_social_graph.follow_user(1, 4)
        test_social_graph.follow_user(2, 3)
        test_social_graph.follow_user(2, 5)
        test_social_graph.follow_user(4, 6)
        test_social_graph.follow_user(4, 3)
        test_social_graph.follow_user(7, 2)
        test_social_graph.follow_user(8, 4)
        self.assertEqual(len(test_social_graph.recommend_mutual_friends(1,5)), 5, "Should be 5")
        self.assertEqual(len(test_social_graph.recommend_mutual_friends(1,3)), 3, "Should be 3")
        self.assertEqual(len(test_social_graph.recommend_mutual_friends(1,7)), 5, "Should be 5")
        self.assertEqual(len(test_social_graph.recommend_mutual_friends(2,5)), 1, "Should be 1")
        self.assertEqual(len(test_social_graph.recommend_mutual_friends(3,5)), 0, "Should be 0")
        self.assertEqual(len(test_social_graph.recommend_mutual_friends(4,5)), 1, "Should be 1")
        self.assertEqual(len(test_social_graph.recommend_mutual_friends(5,5)), 0, "Should be 0")
        self.assertEqual(len(test_social_graph.recommend_mutual_friends(6,5)), 0, "Should be 0")
        self.assertEqual(len(test_social_graph.recommend_mutual_friends(7,5)), 3, "Should be 3")
        self.assertEqual(len(test_social_graph.recommend_mutual_friends(8,5)), 3, "Should be 3")

    def test_get_followers_followers(self):
        # A -> B -> C : Recommending C
        test_social_graph = SocialGraph()
        test_social_graph.follow_user(1, 2)
        test_social_graph.follow_user(1, 4)
        test_social_graph.follow_user(2, 3)
        test_social_graph.follow_user(2, 5)
        test_social_graph.follow_user(4, 6)
        test_social_graph.follow_user(4, 3)
        self.assertEqual(len(test_social_graph.get_followers_followers(1)), 3, "Should be 3")
        self.assertEqual(len(test_social_graph.get_followers_followers(2)), 0, "Should be 0")
        self.assertEqual(len(test_social_graph.get_followers_followers(3)), 0, "Should be 0")
        self.assertEqual(len(test_social_graph.get_followers_followers(4)), 0, "Should be 0")
        self.assertEqual(len(test_social_graph.get_followers_followers(5)), 0, "Should be 0")
        self.assertEqual(len(test_social_graph.get_followers_followers(6)), 0, "Should be 0")

    def test_get_other_users_following_same_user(self):
        # A -> B <- C : Recommeding C
        test_social_graph = SocialGraph()
        test_social_graph.follow_user(1, 2)
        test_social_graph.follow_user(1, 4)
        test_social_graph.follow_user(3, 2)
        test_social_graph.follow_user(4, 2)
        test_social_graph.follow_user(5, 2)
        test_social_graph.follow_user(6, 4)
        self.assertEqual(len(test_social_graph.get_other_users_following_same_user(1)), 3, "Should be 3")
        self.assertEqual(len(test_social_graph.get_other_users_following_same_user(2)), 0, "Should be 0")
        self.assertEqual(len(test_social_graph.get_other_users_following_same_user(3)), 3, "Should be 3")
        self.assertEqual(len(test_social_graph.get_other_users_following_same_user(4)), 3, "Should be 3")
        self.assertEqual(len(test_social_graph.get_other_users_following_same_user(5)), 3, "Should be 3")
        self.assertEqual(len(test_social_graph.get_other_users_following_same_user(6)), 1, "Should be 1")

    def test_get_users_following_mutual_friends(self):
        # A <-> B <- C: Recommending C's
        test_social_graph = SocialGraph()
        test_social_graph.follow_user(1, 2)
        test_social_graph.follow_user(2, 1)
        test_social_graph.follow_user(1, 4)
        test_social_graph.follow_user(4, 1)
        test_social_graph.follow_user(5, 2)
        test_social_graph.follow_user(6, 4)
        self.assertEqual(len(test_social_graph.get_users_following_mutual_friends(1)), 2, "Should be 2")
        self.assertEqual(len(test_social_graph.get_users_following_mutual_friends(2)), 1, "Should be 1")
        self.assertEqual(len(test_social_graph.get_users_following_mutual_friends(4)), 1, "Should be 1")
        self.assertEqual(len(test_social_graph.get_users_following_mutual_friends(5)), 0, "Should be 0")
        self.assertEqual(len(test_social_graph.get_users_following_mutual_friends(6)), 0, "Should be 0")


    def test_get_followees_by_user_id(self):
        test_social_graph = SocialGraph()
        test_social_graph.follow_user(1, 2)
        test_social_graph.follow_user(2, 1)
        test_social_graph.follow_user(1, 4)
        test_social_graph.follow_user(4, 1)
        test_social_graph.follow_user(1, 5)
        test_social_graph.follow_user(1, 6)
        self.assertEqual(len(test_social_graph.get_followees_by_user_id(1)), 2, "Should be 2")
        self.assertEqual(len(test_social_graph.get_followees_by_user_id(2)), 1, "Should be 1")
        self.assertEqual(len(test_social_graph.get_followees_by_user_id(4)), 1, "Should be 1")
        self.assertEqual(len(test_social_graph.get_followees_by_user_id(5)), 1, "Should be 1")
        self.assertEqual(len(test_social_graph.get_followees_by_user_id(6)), 1, "Should be 1")

    def test_get_friends_by_user_id(self):
        test_social_graph = SocialGraph()
        test_social_graph.follow_user(1, 2)
        test_social_graph.follow_user(2, 1)
        test_social_graph.follow_user(1, 4)
        test_social_graph.follow_user(4, 1)
        test_social_graph.follow_user(1, 5)
        test_social_graph.follow_user(1, 6)
        self.assertEqual(len(test_social_graph.get_friends_by_user_id(1)), 2, "Should be 2")
        self.assertEqual(len(test_social_graph.get_friends_by_user_id(2)), 1, "Should be 1")
        self.assertEqual(len(test_social_graph.get_friends_by_user_id(4)), 1, "Should be 1")
        self.assertEqual(len(test_social_graph.get_friends_by_user_id(5)), 0, "Should be 0")
        self.assertEqual(len(test_social_graph.get_friends_by_user_id(6)), 0, "Should be 0")

    def test_follow_user(self):
        test_social_graph = SocialGraph()
        test_social_graph.follow_user(1, 2)
        test_social_graph.follow_user(1, 3)
        test_social_graph.follow_user(1, 4)
        self.assertEqual(len(test_social_graph.follower_relationship[1]), 3, "Should be 3")
        self.assertEqual(len(test_social_graph.follower_relationship[2]), 0, "Should be 0")
        self.assertEqual(len(test_social_graph.follower_relationship[3]), 0, "Should be 0")
        self.assertEqual(len(test_social_graph.follower_relationship[4]), 0, "Should be 0")
        self.assertEqual(len(test_social_graph.followee_relationship[1]), 0, "Should be 0")
        self.assertEqual(len(test_social_graph.followee_relationship[2]), 1, "Should be 1")
        self.assertEqual(len(test_social_graph.followee_relationship[3]), 1, "Should be 1")
        self.assertEqual(len(test_social_graph.followee_relationship[4]), 1, "Should be 1")

    def test_increment_weight(self):
        test_social_graph = SocialGraph()       
        test_social_graph.follow_user(1, 2)
        test_social_graph.increment_weight(1, 2, 5)
        self.assertEqual(test_social_graph.follower_relationship[1][2], 5, "Should be 5")
        self.assertEqual(test_social_graph.followee_relationship[2][1], 5, "Should be 5")

if __name__ == "__main__":
    unittest.main()