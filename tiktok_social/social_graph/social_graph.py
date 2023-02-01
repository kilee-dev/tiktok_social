from collections import defaultdict
from typing import List, DefaultDict, Set
from schema.user import UserIdT

class SocialGraph: 
    def __init__(self):
        self.follower_relationship: DefaultDict[UserIdT, DefaultDict[UserIdT, int]] = defaultdict(lambda: defaultdict(int))
        self.followee_relationship: DefaultDict[UserIdT, DefaultDict[UserIdT, int]] = defaultdict(lambda: defaultdict(int))

    def recommend_mutual_friends(self, user_id: UserIdT, count: int) -> List[UserIdT]:
        return list(
            set.union(
                *[
                    self.get_followers_followers(user_id),
                    self.get_other_users_following_same_user(user_id),
                    self.get_users_following_mutual_friends(user_id)
                ]
            )
        )[:count]

    # A -> B -> C : Recommending C
    def get_followers_followers(self, user_id: UserIdT) -> Set[UserIdT]:
        excluding_user_ids = set(list(self.follower_relationship[user_id].keys()) + [user_id])
        result = set()
        
        for one_hop_follower in self.follower_relationship[user_id].keys():
            for two_hop_follower in self.follower_relationship[one_hop_follower]:
                if two_hop_follower not in excluding_user_ids:
                    result.add(two_hop_follower)

        return result

    # A -> B <- C : Recommeding C
    def get_other_users_following_same_user(self, user_id: UserIdT) -> Set[UserIdT]:
        excluding_user_ids = set(list(self.follower_relationship[user_id].keys()) + [user_id])
        result = set()
        
        # follower list who user_id follow
        for one_hop_follower_id in self.follower_relationship[user_id].keys():
            # followee list who follows the one_hop_follower
            for followee_id in self.followee_relationship[one_hop_follower_id]:
                if followee_id not in excluding_user_ids:
                    result.add(followee_id)
        
        return result

    # A <-> B <- C: Recommending C
    def get_users_following_mutual_friends(self, user_id: UserIdT) -> Set[UserIdT]:
        excluding_user_ids = set(list(self.follower_relationship[user_id].keys()) + [user_id])
        result = set()

        for one_hop_follower in self.follower_relationship[user_id].keys():
            if one_hop_follower in self.followee_relationship[user_id]:
                for follower_id in self.followee_relationship[one_hop_follower].keys():
                    if follower_id not in excluding_user_ids:
                        result.add(follower_id)

        return result
        
    def get_followees_by_user_id(self, user_id: UserIdT) -> List[UserIdT]:
        return list(self.followee_relationship[user_id].keys())
    
    # A <-> B, return all Bs
    def get_friends_by_user_id(self, user_id: UserIdT) -> List[UserIdT]:
        excluding_user_ids = set()
        
        mutual_friends = []
        
        # users who follow user_id and user_id follow back
        for one_hop_follower_id in self.follower_relationship[user_id].keys():
            if user_id in self.follower_relationship[one_hop_follower_id]:
                if one_hop_follower_id not in excluding_user_ids:
                    mutual_friends.append(one_hop_follower_id)

        return mutual_friends

    def follow_user(self, follower_id: UserIdT, followee_id: UserIdT) -> None:
        self.follower_relationship[follower_id][followee_id] = 0 
        self.followee_relationship[followee_id][follower_id] = 0

    def increment_weight(self, follower_id: UserIdT, followee_id: UserIdT, weight: int) -> None:
        self.follower_relationship[follower_id][followee_id] += weight 
        self.followee_relationship[followee_id][follower_id] += weight

        