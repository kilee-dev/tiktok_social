import unittest
from .db import DB
from schema.post import PostIdT, Post
from schema.repost import RepostIdT, Repost

class TestDB(unittest.TestCase):
    def test_create_post(self):
        db = DB()
        db.create_post(Post(1, 1))
        db.create_post(Post(2, 1))
        db.create_post(Post(3, 1))
        self.assertEqual(len(db.posts), 3, "Should be 3")
    
    def test_get_post_by_id(self):
        db = DB()
        db.create_post(Post(1, 1))
        self.assertEqual(db.get_post_by_id(1).author_id, 1, "Should be 1")

    def test_create_repost(self):
        db = DB()
        db.create_repost(Repost(1, 1, 1))
        db.create_repost(Repost(2, 2, 1))
        db.create_repost(Repost(3, 3, 1))
        self.assertEqual(len(db.reposts), 3, "Should be 3")

    def test_get_repost_by_id(self):
        db = DB()
        db.create_repost(Repost(1, 1, 1))
        self.assertEqual(db.get_repost_by_id(1).original_post_id, 1, "Should be 1")
        self.assertEqual(db.get_repost_by_id(1).repost_user_id, 1, "Should be 1")

    def test_user_like_post(self):
        db = DB()
        db.create_post(Post(1, 1))
        db.user_like_post(1, 1)
        self.assertEqual(db.post_likes[(1, 1)] != None, True, "Should be True")

    def test_user_comment_on_post(self):
        db = DB()
        db.create_post(Post(1, 1))
        db.user_comment_on_post(1, 1, "So cool!")
        self.assertEqual(db.post_comments[(1, 1)].content, "So cool!", "Should be So cool!")

    def test_user_share_post(self):
        db = DB()
        db.create_post(Post(1, 1))
        db.user_share_post(1, 1)
        self.assertEqual(db.post_shares[(1, 1)] != None, True, "Should be True")

    def test_user_save_post(self):
        db = DB()
        db.create_post(Post(1, 1))
        db.user_save_post(1, 1)
        self.assertEqual(db.post_saves[(1, 1)] != None, True, "Should be True")

if __name__ == "__main__":
    unittest.main()