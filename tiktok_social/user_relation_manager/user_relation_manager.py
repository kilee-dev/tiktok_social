from user_retriever.facebook_user_retriever import FacebookUserRetriever
from user_retriever.phone_contact_user_retriever import PhoneContactUserRetriever
from social_graph.social_graph import SocialGraph
from schema.user import UserIdT
from typing import List
import random

class UserRelationManager:
    def __init__(self, 
                facebook_user_retriever: FacebookUserRetriever, 
                phone_contact_user_retriever: PhoneContactUserRetriever,
                social_graph: SocialGraph,
    ):
        self.facebook_user_retriever = facebook_user_retriever
        self.phone_contact_user_retriever = phone_contact_user_retriever
        self.social_graph = social_graph

    def import_phone_contacts(self, user_id: UserIdT) -> None:
        self.phone_contact_user_retriever.import_user_friends(user_id)

    def import_facebook_accounts(self, user_id: UserIdT) -> None:
        self.facebook_user_retriever.import_user_friends(user_id)

    def unsync_phone_contacts(self, user_id: UserIdT) -> None:
        self.phone_contact_user_retriever.unsync_user_friends(user_id)

    def unsync_facebook_accounts(self, user_id: UserIdT) -> None:
        self.facebook_user_retriever.unsync_user_friends(user_id)

    def recommend_friends(self, user_id: UserIdT, count: int) -> List[UserIdT]:
        candidates = [
            *self.facebook_user_retriever.recommend_friends(user_id),
            *self.phone_contact_user_retriever.recommend_friends(user_id),
            *self.social_graph.recommend_mutual_friends(user_id, count)
        ]
        random.shuffle(candidates)
        
        return candidates[:count]
