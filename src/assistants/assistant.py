from abc import ABC, abstractmethod


class Assistant(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def ask_assistant(self, question: str) -> str:
        """_summary_

        Args:
            question (str): _description_

        Returns:
            str: _description_
        """
        pass

    @abstractmethod
    def get_system_role(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """
        pass

    @abstractmethod
    def additional_data(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """
        pass
