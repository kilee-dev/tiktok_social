from typing import Dict, List, Set
from schema.user import User, UserIdT

class UserManager:
    def __init__(self):
        self.facebook_account_to_user_id: Dict[str, UserIdT] = dict()
        self.phone_contact_to_user_id: Dict[str, UserIdT] = dict()

    def find_user_ids_by_facebook_accounts(self, facebook_accounts: Set[str]) -> List[UserIdT]:
        user_ids = []
        for facebook_account in facebook_accounts:
            if user_id := self.facebook_account_to_user_id.get(facebook_account, None) is not None:
                user_ids.append(user_id)

        return user_ids

    def find_user_ids_by_phone_contacts(self, phone_contacts: Set[str]) -> List[UserIdT]:
        user_ids = []
        for phone_contact in phone_contacts:
            if phone_contact in self.phone_contact_to_user_id:
                user_ids.append(self.phone_contact_to_user_id[phone_contact])
        
        return user_ids


    def add_user(self, user: User) -> None:
        if user.facebook_account is not None:
            self.facebook_account_to_user_id[user.facebook_account] = user.id
        if user.phone_contact is not None:
            self.phone_contact_to_user_id[user.phone_contact] = user.id
