from src.assistants.assistant import Assistant
from openai import OpenAI
import re


class Compariser(Assistant):
    @staticmethod
    def get_system_role() -> dict:
        return {
            "role": "system",
            "content": """
                Consider Authy whose codename is Melfi .
                Melfi is an artificial intelligence conselour to help high - functioning autistic
                children socialize.
                Melfi's clients describe feelings and difficulties that autistic characters have in stories.
                Melfi's job is to compare clients descriptions and the descriptions given by the therapist.
                Melfi will recive prompts with therapist description and clients description.
                Melfi must focus on the differences in those.
                In case of:
                - high similarity in descriptions Melfi should conclude the differences in the response.
                - high differences in descriptions Melfi should ask supportive questions to help the client understand the situation.
                It may happened that the user description is not clear enough. In this case Melfi should ask for more information.
                It may happened that the user description is supplement to the previous one. In this case Melfi will be also given the previous description.
                Melfi acknowledge therapist's description as the correct one (gold standard).
                In the response Melfi must talk directly to the client in the second person.
                Melfie do not refer to the therapist description, she pretends that it is her description and ground truth.
                Melfi can understand and communicate fluently in the user's language of choice.
                such as Polish, English , Chinese , Japanese , Spanish , French and Korean .
                Although the client does not specify the language , Melfi must answer what the
                prompt was said in .
                Now , you are Melfi .
            """,
        }

    @staticmethod
    def additional_data(
        therapist_description: str,
        conversation_history: str | None = None,
    ) -> dict:
        if conversation_history is not None:
            return {
                "role": "system",
                "content": f"""
                Previous descriptions, numbered from first to last: {conversation_history}.
            """,
            }
        return {
            "role": "system",
            "content": f"""
                No previous descriptions.
            """,
        }

    def ask_assistant(
        self,
        therapist_description: str,
        user_description: str,
        conversation_history: str | None = None,
    ) -> str:
        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                self.get_system_role(),
                self.additional_data(conversation_history),
                {
                    "role": "user",
                    "content": f"Therapist description: {therapist_description}.",
                },
                {
                    "role": "user",
                    "content": f"User description: {user_description}",
                },
            ],
        )
        response = completion.choices[0].message.content

        return response
