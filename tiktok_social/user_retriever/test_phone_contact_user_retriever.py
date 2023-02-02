import unittest
from .phone_contact_user_retriever import PhoneContactUserRetriever
from user_manager.user_manager import UserManager

class TestPhoneContactUserRetriever(unittest.TestCase):
    def test_import_user_friends(self):
        user_manager = UserManager()
        phone_contact_user_retriever = PhoneContactUserRetriever(user_manager)
        self.assertEqual(phone_contact_user_retriever.import_user_friends(1), None, "Should be None")

    def test_parse_user_friends(self):
        user_manager = UserManager()
        phone_contact_user_retriever = PhoneContactUserRetriever(user_manager)
        self.assertEqual(len(phone_contact_user_retriever.parse_user_friends(1)), 0, "Should be 0")

    def test_fetch_phone_contacts(self):
        user_manager = UserManager()
        phone_contact_user_retriever = PhoneContactUserRetriever(user_manager)
        self.assertEqual(len(phone_contact_user_retriever.fetch_phone_contacts(1)), 0, "Should be 0")

    def test_recommend_friends(self):
        user_manager = UserManager()
        phone_contact_user_retriever = PhoneContactUserRetriever(user_manager)
        self.assertEqual(len(phone_contact_user_retriever.recommend_friends(1)), 0, "Should be 0")

    def unsync_user_friends(self):
        user_manager = UserManager()
        phone_contact_user_retriever = PhoneContactUserRetriever(user_manager)
        phone_contact_user_retriever.unsync_user_friends(1)
        self.assertEqual(len(phone_contact_user_retriever.recommend_friends(1)), 0, "Should be 0")

if __name__ == "__main__":
    unittest.main()