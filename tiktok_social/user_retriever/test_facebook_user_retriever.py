import unittest
from .facebook_user_retriever import FacebookUserRetriever
from user_manager.user_manager import UserManager

class TestFacebookUserRetriever(unittest.TestCase):
    def test_import_user_friends(self):
        user_manager = UserManager()
        facebook_user_retriever = FacebookUserRetriever(user_manager)
        self.assertEqual(facebook_user_retriever.import_user_friends(1), None, "Should be None")

    def test_parse_user_friends(self):
        user_manager = UserManager()
        facebook_user_retriever = FacebookUserRetriever(user_manager)
        self.assertEqual(len(facebook_user_retriever.parse_user_friends(1)), 0, "Should be 0")

    def test_fetch_facebook_friend_accounts(self):
        user_manager = UserManager()
        facebook_user_retriever = FacebookUserRetriever(user_manager)
        self.assertEqual(len(facebook_user_retriever.fetch_facebook_friend_accounts(1)), 0, "Should be 0")

    def test_recommend_friends(self):
        user_manager = UserManager()
        facebook_user_retriever = FacebookUserRetriever(user_manager)
        self.assertEqual(len(facebook_user_retriever.recommend_friends(1)), 0, "Should be 0")

    def unsync_user_friends(self):
        user_manager = UserManager()
        facebook_user_retriever = FacebookUserRetriever(user_manager)
        facebook_user_retriever.unsync_user_friends(1)
        self.assertEqual(len(facebook_user_retriever.recommend_friends(1)), 0, "Should be 0")

if __name__ == "__main__":
    unittest.main()