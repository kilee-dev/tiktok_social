from collections import defaultdict
from typing import DefaultDict
from schema.post import PostIdT

class PostCounterCache:
    def __init__(self):
        self.post_comments_counts: DefaultDict[PostIdT, int] = defaultdict(int)
        self.post_likes_counts: DefaultDict[PostIdT, int] = defaultdict(int)
        self.post_saves_counts: DefaultDict[PostIdT, int] = defaultdict(int)
        self.post_shares_counts: DefaultDict[PostIdT, int] = defaultdict(int)

    def increment_post_comments_counts(self, post_id: PostIdT) -> None:
        self.post_comments_counts[post_id] += 1

    def decrement_post_comments_counts(self, post_id: PostIdT) -> None:
        self.post_comments_counts[post_id] -= 1

    def increment_post_likes_counts(self, post_id: PostIdT) -> None:
        self.post_likes_counts[post_id] += 1

    def decrement_post_likes_counts(self, post_id: PostIdT) -> None:
        self.post_likes_counts[post_id] -= 1

    def increment_post_saves_counts(self, post_id: PostIdT) -> None:
        self.post_saves_counts[post_id] += 1

    def decrement_post_saves_counts(self, post_id: PostIdT) -> None:
        self.post_saves_counts[post_id] -= 1

    def increment_post_shares_counts(self, post_id: PostIdT) -> None:
        self.post_shares_counts[post_id] += 1

    def decrement_post_shares_counts(self, post_id: PostIdT) -> None:
        self.post_shares_counts[post_id] -= 1