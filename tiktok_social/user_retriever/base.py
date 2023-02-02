from abc import ABC, abstractmethod
from typing import DefaultDict, Set, List
from collections import defaultdict
from schema.user import UserIdT
from user_manager.user_manager import UserManager

class BaseUserRetriever(ABC):
    def __init__(self, user_manager: UserManager):
        self.user_retriever_candidates: DefaultDict[UserIdT, Set[UserIdT]] = defaultdict(set)
        self.user_manager = user_manager

    @abstractmethod
    def parse_user_friends(self, user_id: UserIdT) -> Set[UserIdT]:
        raise NotImplementedError()

    def import_user_friends(self, user_id: UserIdT) -> None:
        self.user_retriever_candidates[user_id] = self.parse_user_friends(user_id)

    def recommend_friends(self, user_id: UserIdT) -> List[UserIdT]:
        return list(self.user_retriever_candidates[user_id])
    
    def unsync_user_friends(self, user_id: UserIdT) -> None:
        del self.user_retriever_candidates[user_id]
    
