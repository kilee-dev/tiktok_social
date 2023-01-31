from dataclasses import dataclass
from typing import Optional, TypeVar

UserIdT = TypeVar('UserIdT')

@dataclass
class User:
    id: UserIdT
    facebook_account: Optional[str] = None
    phone_contact: Optional[str] = None