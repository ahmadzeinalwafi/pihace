from abc import ABC, abstractmethod

class BaseChecker(ABC):
    @abstractmethod
    def check(self):
        """
        Should return True or (False, 'error message')
        """
        pass
