from abc import ABC, abstractmethod


class AdminInterface(ABC):

    @abstractmethod
    def activate_account(self,data):
        pass

    @abstractmethod
    def suspend_account(self,data):
        pass

    @abstractmethod
    def close_account(self,data):
        pass

    @abstractmethod
    def view_audit_logs(self):
        pass