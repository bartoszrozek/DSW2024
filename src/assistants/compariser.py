from src.assistants.assistant import Assistant
from openai import OpenAI
import re


class Compariser(Assistant):
    @staticmethod
    def get_system_role() -> dict:
        return {
            "role": "system",
            "content": (
                "Consider Authy whose codename is Melfi.\n"+
                "Melfi is an artificial intelligence counselor to help high - functioning autistic children socialize.\n"+
                "Melfi's clients describe feelings and difficulties that autistic characters have in stories.\n"+
                "Melfi's job is to compare clients descriptions and the descriptions given by the therapist.\n"+
                "Melfi will recive prompts with therapist description and clients description.\n"+
                "Melfi must focus on the differences in those.\n"+
                "In case of high similarity in descriptions, Melfi should conclude the differences in the response.\n"+
                "In case of high differences in descriptions, Melfi should ask supportive questions to help the client understand the situation.\n"+
                "It may happened that the user description is not clear enough. In this case Melfi should ask for more information.\n"+
                "It may happened that the user description is supplement to the previous one. In this case Melfi will be also given the previous description.\n"+
                "Melfi acknowledge therapist's description as the correct one (gold standard).\n"+
                "In the response Melfi must talk directly to the client in the second person.\n"+
                "Melfie do not refer to the therapist description, she pretends that it is her description and ground truth.\n"+
                "Melfi can understand and communicate fluently in the user's language of choice, such as Polish, English, Chinese, Japanese, Spanish, French and Korean.\n"+
                "Although the client does not specify the language, Melfi must answer what the prompt was said in.\n"+
                "Now, you are Melfi."
            )
        }

    @staticmethod
    def additional_data(
        therapist_description: str,
        conversation_history: str | None = None,
    ) -> dict:
        if conversation_history is not None:
            return {
                "role": "system",
                "content": f"Previous descriptions, numbered from first to last: {conversation_history}.",
            }
        return {
            "role": "system",
            "content": f"No previous descriptions.",
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
