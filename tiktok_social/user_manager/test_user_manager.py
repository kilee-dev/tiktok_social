import unittest
from .user_manager import UserManager
from schema.user import User

class TestUserManager(unittest.TestCase):
    def test_find_user_ids_by_facebook_account(self):
        test_user_manager = UserManager()
        new_user = User(1, "giung.lee@gmail.com")
        test_user_manager.add_user(new_user)
        self.assertEqual(test_user_manager.find_user_ids_by_facebook_accounts(set([new_user.facebook_account])), [new_user.id], "Should be [1]")
        
    def test_find_user_ids_by_phone_contacts(self):
        test_user_manager = UserManager()
        new_user = User(1, "giung.lee@gmail.com", "123-456-7890")
        test_user_manager.add_user(new_user)
        self.assertEqual(test_user_manager.find_user_ids_by_phone_contacts(set([new_user.phone_contact])), [new_user.id], "Should be [1]")

    def test_add_user(self):
        test_user_manager = UserManager()
        test_user_1 = User(1)
        test_user_2 = User(2)
        test_user_3 = User(3)
        test_user_manager.add_user(test_user_1)
        test_user_manager.add_user(test_user_2)
        test_user_manager.add_user(test_user_3)
        self.assertEqual(len(test_user_manager.find_user_ids_by_facebook_accounts(set([test_user_1.facebook_account, test_user_2.facebook_account, test_user_3.facebook_account]))), 0, "Should be 0")
        self.assertEqual(len(test_user_manager.find_user_ids_by_phone_contacts(set([test_user_1.phone_contact, test_user_2.phone_contact, test_user_3.phone_contact]))), 0, "Should be 0")

if __name__ == "__main__":
    unittest.main()