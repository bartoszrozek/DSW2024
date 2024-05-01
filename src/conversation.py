from src.structs import Message


class Conversation:
    def __init__(self) -> None:
        self._messages = []

    def new_message(self, text, author) -> None:
        self._messages.append(
            Message(
                id=len(self._messages),
                text=text,
                author=author,
            )
        )

    def new_message_from_instance(self, message: Message) -> None:
        message.id = len(self._messages)
        self._messages.append(message)

    def last_message(self) -> Message:
        if len(self._messages) == 0:
            return
        return self._messages[-1]
