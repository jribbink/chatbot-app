from abc import ABC, abstractmethod


class QueryFilter(ABC):
    @abstractmethod
    def parse(current_query, original_query):
        pass
