from abc import ABC, abstractmethod


class PasswordServiceInterface(ABC):
    @abstractmethod
    def save_credentials(self,user_identity, data):
        pass

    @abstractmethod
    def retrieve_credentials(self, user_identity):
        pass

    @abstractmethod
    def delete_credentials(self, user_identity, website):
        pass

    @abstractmethod
    def update_credentials(self, user_identity, data, website):
        pass

    @abstractmethod
    def save_detected_credentials(self, user_identity, data):
        pass

