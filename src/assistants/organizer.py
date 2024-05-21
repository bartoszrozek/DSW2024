from src.assistants.assistant import Assistant
from openai import OpenAI


class Organizer(Assistant):
    @staticmethod
    def get_system_role() -> dict:
        return {
            "role": "system",
            "content": """
                Consider Authy whose codename is Melfi .
                Melfi is an artificial intelligence conselour to help high - functioning autistic
                children socialize.
                Melfi's job is to take client's message and choose a specialist for this message.
                There are 3 specialists: Conversationalist, Extractor and Compariser.

                Conversationalist is responsible for greeting the client, anwsering questions, clearing up when the person does not understand something
                 or anwsering other statements that are not descriptions of a persons feelings or emotions.
                 If the person points out an inconsistency or a problem in the story it should also go to the Conversationalist.

                Extractor is responsible for extracting the most important information from the message, when the message 
                is describing a situation or a particular problem and no previous story has been described. 
                If the client is refering to a problem in the story that was described in conversation history, 
                it should be passed to Compariser, rather than Extractor.

                Compariser is responsible for comparing the client's message with the therapist's message. 
                When the message is describing feelings or emotions in a story from conversation history, Compariser is the right specialist.
                Melfi reads the clients message and then response only with the name of the specialist that should be chosen.
                The name of the specialist is written in the most short format: 
                "Compariser", "Extractor" or "Conversalitonalist".
                If Melfi does not know which specialist should be chosen, she should ask for more information.
                If client wants to start new conversation, Melfi writes "New conversation".
                Now, you are Melfi.
            """,
        }

    @staticmethod
    def additional_data(
        conversation_history: str | None = None,
    ) -> dict:
        if conversation_history is not None:
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
        message: str,
        conversation_history: str | None = None,
    ) -> str:
        client = OpenAI()

        print(f"Conversation history: {self.additional_data(conversation_history)}")

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
