from dataclasses import dataclass
from shiny import ui
from typing import Literal


@dataclass
class Message:
    """Class for message info."""

    text: str
    author: Literal["user", "chat"]
    id: int = None

    def generate_ui(self):
        return ui.div(
            ui.div(self.author, class_="message-author"),
            ui.div(self.text, class_="message-body"),
            class_=f"{self.author}-message",
        )
