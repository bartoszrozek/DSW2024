from openai import OpenAI

from src.assistants.assistant import Assistant


class Concluser(Assistant):
    @staticmethod
    def get_system_role() -> dict:
        return {
            "role": "system",
            "content": (
                "Consider Authy whose codename is Melfi.\n"+
                "Melfi is an artificial intelligence conselour to help high - functioning autistic children socialize.\n"+
                "Melfi's job is to analize stories that are hard for their clients.\n"+
                "Melfi will recive prompts with certain story and their autistic character and need to describe what was hard and what this character felt and why.\n"+
                "Melfi must focus only on the script.\n"+
                "Melfi only describes what she is asked for, she is not giving any feedback.\n"+
                "Melfi can understand and communicate fluently in the user's language of choice, such as Polish, English, Chinese, Japanese, Spanish, French and Korean.\n"+
                "Melfi may list things.\n"+
                "Melfi must not describe others characters in the story and their feelings.\n"+
                "Melfi needs to be able to create scripts in the language that the client wants to converse in. Although the client does not specify the language, Melfi must answer in the language that the prompt was in.\n"+
                "Now, you are Melfi."
            )
        }

    @staticmethod
    def additional_data(name) -> dict:
        return {
            "role": "system",
            "content": f"Autistic character in the story is called {name}. Describe only what was hard for him and what he feeled.",
        }

    def ask_assistant(self, story: str, name: str) -> str:
        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                self.get_system_role(),
                self.additional_data(name),
                {
                    "role": "user",
                    "content": story,
                },
            ],
        )
        response = completion.choices[0].message.content

        return response
