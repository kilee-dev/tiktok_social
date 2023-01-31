import unittest
from user_manager.user_manager import UserManager
from user_retriever.facebook_user_retriever import FacebookUserRetriever
from user_retriever.phone_contact_user_retriever import PhoneContactUserRetriever
from social_graph.social_graph import SocialGraph
from .user_relation_manager import UserRelationManager


class TestUserRelationManager(unittest.TestCase):
    def test_import_phone_contacts(self):
        user_manager = UserManager()
        facebook_user_retriever = FacebookUserRetriever(user_manager)
        phone_contact_user_retriever = PhoneContactUserRetriever(user_manager)
        social_graph = SocialGraph()

        user_relation_manager = UserRelationManager(
            facebook_user_retriever,
            phone_contact_user_retriever,
            social_graph
        )

        self.assertEqual(user_relation_manager.import_phone_contacts(1), None, "Should be None")

    def test_import_facebook_account(self):
        user_manager = UserManager()
        facebook_user_retriever = FacebookUserRetriever(user_manager)
        phone_contact_user_retriever = PhoneContactUserRetriever(user_manager)
        social_graph = SocialGraph()

        user_relation_manager = UserRelationManager(
            facebook_user_retriever,
            phone_contact_user_retriever,
            social_graph
        )

        self.assertEqual(user_relation_manager.import_facebook_accounts(1), None, "Should be None")

    def test_unsync_phone_contacts(self):
        user_manager = UserManager()
        facebook_user_retriever = FacebookUserRetriever(user_manager)
        phone_contact_user_retriever = PhoneContactUserRetriever(user_manager)
        social_graph = SocialGraph()

        user_relation_manager = UserRelationManager(
            facebook_user_retriever,
            phone_contact_user_retriever,
            social_graph
        )

        user_relation_manager.import_phone_contacts(1)

        self.assertEqual(user_relation_manager.unsync_phone_contacts(1), None, "Should be None")


    def test_unsync_facebook_accounts(self):
        user_manager = UserManager()
        facebook_user_retriever = FacebookUserRetriever(user_manager)
        phone_contact_user_retriever = PhoneContactUserRetriever(user_manager)
        social_graph = SocialGraph()

        user_relation_manager = UserRelationManager(
            facebook_user_retriever,
            phone_contact_user_retriever,
            social_graph
        )

        user_relation_manager.import_facebook_accounts(1)

        self.assertEqual(user_relation_manager.unsync_facebook_accounts(1), None, "Should be None")


    def test_recommend_friends(self):
        user_manager = UserManager()
        facebook_user_retriever = FacebookUserRetriever(user_manager)
        phone_contact_user_retriever = PhoneContactUserRetriever(user_manager)
        social_graph = SocialGraph()
        social_graph.follow_user(1, 2)
        social_graph.follow_user(2, 3)
        social_graph.follow_user(2, 4)
        social_graph.follow_user(1, 5)
        social_graph.follow_user(5, 6)
        social_graph.follow_user(5, 7)

        user_relation_manager = UserRelationManager(
            facebook_user_retriever,
            phone_contact_user_retriever,
            social_graph
        )

        self.assertEqual(len(user_relation_manager.recommend_friends(1, 4)), 4, "Should be 4")


if __name__ == "__main__":
    unittest.main()