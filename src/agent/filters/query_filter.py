from abc import ABC, abstractmethod

from filters.agent_filter import AgentFilter


class QueryFilter(AgentFilter):
    @abstractmethod
    def parse(current_query, original_query):
        pass
