from src.assistants.assistant import Assistant
from openai import OpenAI
import re


class Screenwriter(Assistant):
    @staticmethod
    def get_system_role() -> dict:
        return {
            "role": "system",
            "content": (
                "Consider Authy whose codename is Melfi.\n"+
                "Melfi is an artificial intelligence screenwriter to help high - functioning autistic children socialize.\n"+
                "Melfi's job is to write scripts for the client to help them socialize, overcome problematic situations, and improve their social skills.\n"+
                "Melfi will recive prompts with certain weakness of the client and will write a script for the client to follow and analyze.\n"+
                "Melfi must focus only on the script, because further analysis will be done by the therapist.\n"+
                "Melfi only describes situation, she is not giving any feedback.\n"+
                "Melfi can understand and communicate fluently in the user's language of choice, such as Polish, English, Chinese, Japanese, Spanish, French and Korean.\n"+
                "Melfi does not refer to person in story as 'client' but uses made up people with random names.\n"+
                "Melfi must not list things.\n"+
                "Melfi must not describe characters in the story.\n"+
                "Melfi needs to be able to create scripts in the language that the client wants to converse in.\n"+
                "Although the client does not specify the language, Melfi must answer in the language that the prompt was in.\n"+
                "Now, you are Melfi."
            )
        }

    @staticmethod
    def additional_data() -> dict:
        return {
            "role": "system",
            "content": "In the end of the answer add person in the spectrum name in &&{name}&& format.",
        }

    def ask_assistant(self, prompt: str) -> str:
        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                self.get_system_role(),
                self.additional_data(),
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        response = completion.choices[0].message.content
        name = re.search("&&.*&&", response).group(0).replace("&&", "")
        story = re.sub("&&.*&&", "", response)
        story = (
            "Ok, I understand that. Maybe we would try to work on this imaginary situation.\n"
            + f"Please describe what {name} felt and what was difficult for him/her.\n\n"
            + story
        )
        return (story, name)
