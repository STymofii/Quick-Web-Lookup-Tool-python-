from abc import ABC, abstractmethod

class Engine(ABC):
    @abstractmethod
    def search(self, query: str, language_code: str = "ru") -> str:
        pass