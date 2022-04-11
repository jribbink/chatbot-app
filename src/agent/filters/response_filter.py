from abc import ABC, abstractmethod

from filters.agent_filter import AgentFilter


class ResponseFilter(AgentFilter):
    @abstractmethod
    def parse(current_repsonse, original_response, query):
        pass
