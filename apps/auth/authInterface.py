import abc
from abc import abstractmethod, ABC


class AuthInterface(ABC):
    @abstractmethod
    def register(self, data):
        pass

    @abstractmethod
    def login(self, data):
        pass

    @abstractmethod
    def forget_password(self, data):
        pass

    @abstractmethod
    def reset_password(self, data):
        pass

    @abstractmethod
    def logout(self, data):
        pass


