from abc import abstractmethod, ABC


class EmailServiceInterface(ABC):


    @abstractmethod
    def send_email(self, to_emil:str, subject:str, message:str):
        pass