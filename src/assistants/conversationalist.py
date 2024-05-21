from src.assistants.assistant import Assistant
from openai import OpenAI


class Conversationalist(Assistant):
    def get_system_role(self) -> dict:
        return {
            "role": "system",
            "content": (
                "Consider Authy whose codename is Melfi.\n"+
                "Melfi is an artificial intelligence conselour to help high - functioning autistic children socialize.\n"+
                "Melfi's clients can ask questions regarding the way chat-bot therapy works: then he should instruct the user that he is here to help him practice social skills and ask what types of situations the client struggles with.\n"+
                "Melfi's clients can have questions about the story that they received or ask to specify something about a previously received message.\n"+
                "If the person points out an inconsistency or a problem in the story Melfi should review the problem and correct it in the story and then present it to the client again.\n"+
                "Melfi should try to help them as well as they can based on the history of the conversation.\n"+
                "Melfi can understand and communicate fluently in English.\n"+
                "In the response Melfi must talk directly to the client in the second person.\n"+
                "Now, you are Melfi."
            )
        }


    @staticmethod
    def additional_data(
        conversation_history: str | None = None,
    ) -> dict:
        if conversation_history is not None:
            return {
                "role": "system",
                "content": f"Previous messages, numbered from first to last: {conversation_history}.",
            }
        return {
            "role": "system",
            "content": "No previous messages.",
        }

    def ask_assistant(
        self,
        message: str,
        conversation_history: str | None = None,
    ) -> str:
        client = OpenAI()

        #print(f"Conversation history: {self.additional_data(conversation_history)}")

        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                self.get_system_role(),
                {
                    "role": "user",
                    "content": f"Clients message: {message}",
                },
                self.additional_data(conversation_history)
            ],
        )
        response = completion.choices[0].message.content

        return response