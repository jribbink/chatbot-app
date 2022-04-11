from abc import ABC, abstractmethod


class AgentFilter(ABC):
    def __init__(self, parent):
        self.parent = parent

    def request_response(self, prompt, response_function):
        self.parent.pending_responses.append((prompt, response_function,))
