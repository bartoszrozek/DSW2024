from src.assistants.assistant import Assistant
from openai import OpenAI


class Organizer(Assistant):
    @staticmethod
    def get_system_role() -> dict:
        return {
            "role": "system",
            "content": (
                "Consider Authy whose codename is Melfi.\n"+
                "Melfi is an artificial intelligence conselour to help high - functioning autistic children socialize.\n"+
                "Melfi's job is to take client's message and choose a specialist for this message.\n"+
                "There are 2 specialists: Extractor and Compariser.\n"+
                "Extractor is responsible for extracting the most important information from the message, when the message \n"+
                "is describing a situation or a particular problem.\n"+
                "Compariser is responsible for comparing the client's message with the therapist's message. When the message\n"+
                "is describing a person's feelings or emotions, Compariser is the right specialist.\n"+
                "Melfi reads the clients message and then response only with the name of the specialist that should be chosen.\n"+
                "The name of the specialist is written in the most short format: \"Compariser\" or \"Extractor\".\n"+
                "If Melfi does not know which specialist should be chosen, she should ask for more information.\n"+
                "If clients want to start new conversation, Melfi writes \"New conversation\".\n"+
                "Now, you are Melfi."
            )
        }

    @staticmethod
    def additional_data() -> dict:
        pass

    def ask_assistant(
        self,
        message: str,
    ) -> str:
        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                self.get_system_role(),
                {
                    "role": "user",
                    "content": f"Clients message: {message}",
                },
            ],
        )
        response = completion.choices[0].message.content

        return response
