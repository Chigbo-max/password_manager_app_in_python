from abc import ABC, abstractmethod


class PasswordServiceInterface(ABC):
    @abstractmethod
    def save_credentials(self,user_identity, data):
        pass

    @abstractmethod
    def retrieve_credentials(self, data):
        pass

    @abstractmethod
    def delete_credentials(self, data):
        pass
