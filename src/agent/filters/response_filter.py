from abc import ABC, abstractmethod


class ResponseFilter(ABC):
    @abstractmethod
    def parse(current_repsonse, original_response, query):
        pass
