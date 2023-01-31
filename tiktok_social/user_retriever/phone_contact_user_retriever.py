from user_retriever.base import BaseUserRetriever
from schema.user import UserIdT
from typing import Set
from user_manager.user_manager import UserManager

class PhoneContactUserRetriever(BaseUserRetriever):
    def __init__(self, user_manager: UserManager):
        super().__init__(user_manager)

    def parse_user_friends(self, user_id: UserIdT) -> Set[UserIdT]:
        return self.user_manager.find_user_ids_by_phone_contacts(self.fetch_phone_contacts(user_id))

    def fetch_phone_contacts(self, user_id: UserIdT) -> Set[str]:
        return set()