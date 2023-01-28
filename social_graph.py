"""
Goal: Building RelationshipGraph
Major Requirement/Key Problems
- Importing phone contact and facebook friends(-> Building social graph)
- Unsyncing phone contact and facebook friends(-> deleting the social graph)
- Based on the socialGraph, recommending "suggested accounts"
  + Mutual friends

Directed(Imported) Graph
A -> B(phone contact friend): B's phone contact is imported from A

PhoneContactSocialGraph
- Graph where nodes indicate each user and edges indicate "imported" contact(potential friend relationship) 
FacebookSocialGraph
- Graph where nodes indicate each user and edges indicate "imported" contact(potential friend relationship) 

SocialGraph
- facebook_social_graph: 
- phone_contact_social_graph
"""
from collections import defaultdict
from typing import List, Set

class SocialGraph:
    def __init__(self):
        """
        self.facebook_social_graph["giung.lee"] ={"jiahua.wang", "phillip.teng", ....}
        
        user_1 = User(1, "giung.lee")
        self.facebook_social_graph[user_1] ={"jiahua.wang", "phillip.teng", ....}
        """
        self.facebook_social_graph = defaultdict(set)
        self.phone_contact_social_graph = defaultdict(set)
        
        self.facebook_account_to_tiktok_user_id = defaultdict(int)
        self.phone_contact_to_tiktok_user_id = defaultdict(int)
        
        self.tiktok_user_id_facebook_account = defaultdict(str)
        self.tiktok_user_id_phone_contact = defaultdict(str)
    
    def register_phone_contact(self, user_id:int, phone_number:str) -> None:
        self.tiktok_user_id_phone_contact[user_id] = phone_number
        self.phone_contact_to_tiktok_user_id[phone_number] = user_id
        
    def register_facebook_account(self, user_id:int, facebook_account:str) -> None:
        self.tiktok_user_id_facebook_account[user_id] = facebook_account
        self.facebook_account_to_tiktok_user_id[facebook_account] = user_id
        
    def import_phone_contact(self, importing_user_phone_contact: str, phone_contacts:List[str]) -> None:
        self.phone_contact_social_graph[importing_user_phone_contact] = self.phone_contact_social_graph[importing_user_phone_contact].union(set(phone_contacts))
        
    def import_facebook_friends(self, importing_user_facebook_account: str, facebook_friends:List[str]) -> None:
        self.facebook_social_graph[importing_user_facebook_account] = self.facebook_social_graph[importing_user_facebook_account].union(set(facebook_friends))

    def unsync_phone_contact(self, unsync_user_phone_contact: str) -> None:
        self.phone_contact_social_graph[unsync_user_phone_contact] = set()
        
    def unsync_facebook_friends(self, unsync_facebook_account: str) -> None:
        self.facebook_social_graph[unsync_facebook_account] = set()
        
    def query_imported_phone_contacts(self, user_phone_contact: str) -> Set[str]:
        return self.phone_contact_social_graph[user_phone_contact]
    
    def query_imported_facebook_accounts(self, user_facebook_account: str) -> Set[str]:
        return self.facebook_social_graph[user_facebook_account]
        
    def recommend_friends(self, user_id:int) -> List[int]:
        user_facebook_account = self.tiktok_user_id_facebook_account[user_id]
        user_phone_contact = self.tiktok_user_id_phone_contact[user_id]
        
        candidates = set()
        
        # collect candidates from facebook mutual friends
        for candidate_facebook_account in list(self.facebook_social_graph[user_facebook_account]):
            if user_facebook_account in self.facebook_social_graph[candidate_facebook_account]:
                candidates.add(self.facebook_account_to_tiktok_user_id[candidate_facebook_account])
        
        # collect candidates from phone contacts mutual friends
        for candidate_phone_contact in list(self.phone_contact_social_graph[user_phone_contact]):
            if user_phone_contact in self.phone_contact_social_graph[candidate_phone_contact]:
                candidates.add(self.phone_contact_to_tiktok_user_id[candidate_phone_contact])
                
        return list(candidates)
        

class User:
    def __init__(self, user_id:int, phone_number: str, facebook_account:str):
        self.user_id = user_id
        self.phone_number = phone_number
        self.facebook_account = facebook_account
        
        
socialGraph = SocialGraph()

testUser1 = User(1, "893-231-2312", "giung.lee")
testUser2 = User(2, "324-123-9371", "phillip.teng")
testUser3 = User(3, "001-023-5714", "jiahua.wang")
testUser4 = User(4, "882-123-3423", "lei.su")

# registering phone number
socialGraph.register_phone_contact(testUser1.user_id, testUser1.phone_number)
socialGraph.register_phone_contact(testUser2.user_id, testUser2.phone_number)
socialGraph.register_phone_contact(testUser3.user_id, testUser3.phone_number)
socialGraph.register_phone_contact(testUser4.user_id, testUser4.phone_number)

# registering facebook account
socialGraph.register_facebook_account(testUser1.user_id, testUser1.facebook_account)
socialGraph.register_facebook_account(testUser2.user_id, testUser2.facebook_account)
socialGraph.register_facebook_account(testUser3.user_id, testUser3.facebook_account)
socialGraph.register_facebook_account(testUser4.user_id, testUser4.facebook_account)

# importing phone contacts
# user1 -> set(user2, user3, user4)
socialGraph.import_phone_contact(testUser1.phone_number, [testUser2.phone_number, testUser3.phone_number, testUser4.phone_number])
# user2 -> set(user1, user3)
socialGraph.import_phone_contact(testUser2.phone_number, [testUser1.phone_number, testUser3.phone_number])
# user3 -> set(user1)
socialGraph.import_phone_contact(testUser3.phone_number, [testUser1.phone_number])

# user1 -> set(user2, user3)
socialGraph.import_facebook_friends(testUser1.facebook_account, [testUser2.facebook_account, testUser3.facebook_account])
# user2 -> set(user1, user3, user4)
socialGraph.import_facebook_friends(testUser2.facebook_account, [testUser1.facebook_account, testUser3.facebook_account, testUser4.facebook_account])
# user3 -> set(user1)
socialGraph.import_facebook_friends(testUser3.facebook_account, [testUser1.facebook_account])

assert len(socialGraph.query_imported_phone_contacts(testUser1.phone_number)) == 3
assert len(socialGraph.query_imported_phone_contacts(testUser2.phone_number)) == 2
assert len(socialGraph.query_imported_phone_contacts(testUser3.phone_number)) == 1

assert len(socialGraph.query_imported_facebook_accounts(testUser1.facebook_account)) == 2
assert len(socialGraph.query_imported_facebook_accounts(testUser2.facebook_account)) == 3
assert len(socialGraph.query_imported_facebook_accounts(testUser3.facebook_account)) == 1

assert len(socialGraph.recommend_friends(testUser1.user_id)) == 2
assert len(socialGraph.recommend_friends(testUser2.user_id)) == 1
assert len(socialGraph.recommend_friends(testUser3.user_id)) == 1

socialGraph.unsync_phone_contact(testUser1.phone_number)
socialGraph.unsync_facebook_friends(testUser1.facebook_account)

assert len(socialGraph.query_imported_phone_contacts(testUser1.phone_number)) == 0
assert len(socialGraph.query_imported_facebook_accounts(testUser1.facebook_account)) == 0