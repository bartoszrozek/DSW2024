from src.assistants.assistant import Assistant
from openai import OpenAI


class Conversalionalist(Assistant):
    def get_system_role(self) -> dict:
        return {
            "role": "system",
            "content": """
                Consider Authy whose codename is Melfi.
                Melfi is an artificial intelligence conselour to help high - functioning autistic children socialize.
                Melfi's clients can ask questions regarding the way chat-bot therapy works.
                Melfi's clients can have questions about the story that they received or ask to specify something about a previously received message.
                Melfi should try to help them as well as they can based on the history of the conversation.
                In the response Melfi must talk directly to the client in the second person.
                Now, you are Melfi.
            """,
        }


    @staticmethod
    def additional_data(
        conversation_history: str | None = None,
    ) -> dict:
        if conversation_history is not None:
            print({
                "role": "system",
                "content": f"""
                Previous messages, numbered from first to last: {conversation_history}.
            """,
            })
            return {
                "role": "system",
                "content": f"""
                Previous messages, numbered from first to last: {conversation_history}.
            """,
            }
        return {
            "role": "system",
            "content": f"""
                No previous messages.
            """,
        }

    def ask_assistant(
        self,
        prompt: str,
        conversation_history: str | None = None,
    ) -> str:
        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                self.get_system_role(),
                prompt,
                self.additional_data(conversation_history)
            ],
        )
        response = completion.choices[0].message.content

        return response
