from user_retriever.base import BaseUserRetriever
from typing import Set
from schema.user import UserIdT
from user_manager.user_manager import UserManager

class FacebookUserRetriever(BaseUserRetriever):
    def __init__(self, user_manager: UserManager):
        super().__init__(user_manager)
    
    def parse_user_friends(self, user_id: UserIdT) -> Set[UserIdT]:
        return self.user_manager.find_user_ids_by_facebook_accounts(self.fetch_facebook_friend_accounts(user_id))

    def fetch_facebook_friend_accounts(self, user_id: UserIdT) -> Set[str]:
        return set()
