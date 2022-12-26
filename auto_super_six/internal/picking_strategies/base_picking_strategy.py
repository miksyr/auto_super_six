from abc import ABC, abstractmethod
from typing import List

from betfair_api_client.datamodel.runner import Runner


class BasePickingStrategy(ABC):
    @abstractmethod
    def pick_selection(self, runners: List[Runner]) -> Runner:
        pass
