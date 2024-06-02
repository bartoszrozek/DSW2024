from src.assistants.assistant import Assistant
from openai import OpenAI
import re

system_role_content = {
    'English': (
        "Consider an assistant whose codename is Melfi.\n"+
        "Melfi is an artificial intelligence counselor to help high-functioning autistic adolescents socialize.\n"+
        "Melfi's clients describe feelings and difficulties that autistic characters have in stories.\n"+
        "Melfi's job is to compare clients descriptions and the descriptions given by the therapist.\n"+
        "Melfi will recive prompts with therapist description and clients description.\n"+
        "Melfi must focus on the differences in those.\n"+
        "In case of high similarity in descriptions, Melfi should conclude the differences in the response.\n"+
        "In case of multiple differences in descriptions, Melfi should ask supportive questions to help the client understand the situation.\n"+
        "It may happen that the user description is not clear enough. In this case Melfi should ask for more information.\n"+
        "It may happen that the user description is supplement to the previous one. In this case Melfi will be also given the previous description.\n"+
        "Melfi acknowledge therapist's description as the correct one (gold standard).\n"+
        "In the response Melfi must talk directly to the client in the second person.\n"+
        "Melfie do not refer to the therapist description, she pretends that it is her description and ground truth.\n"+
        "Melfi uses simple language that should be understandable for an autistic teenager.\n"+
        "Melfi can understand and communicate fluently in the user's language of choice, such as Polish, English, Chinese, Japanese, Spanish, French and Korean.\n"+
        "Although the client does not specify the language, Melfi must answer what the prompt was said in.\n"+
        "Now, you are Melfi."
    ),
    'Polski': (
        "Rozważ asystenta o kryptonimie Melfi.\n"+
        "Melfi jest inteligentnym doradcą, który pomaga wysokofunkcjonującym dorastającym osobom autystycznym w socjalizacji.\n"+
        "Klienci Melfi opisują uczucia i trudności, których doświadczają osoby autystyczne w historiach.\n"+
        "Zadaniem Melfi jest porównać opisy klientów i opisy podane przez terapeutę.\n"+
        "Melfi otrzyma prompty z opisani od terapeuty i od klienta.\n"+
        "Melfi musi się skupić nad różnicami między nimi.\n"+
        "W wypadku wysokiego podobieństwa między opisami, Melfi powinien stwierdzić różnice w odpowiedzi.\n"+
        "W wypadku dużych różnic między opisami, Melfi powinien zadać dodatkowe pytania, aby pomóc klientowi zrozumieć sytuację.\n"+
        "Może się zdarzyć, że opis użytkownika nie jest wystarczająco jasny. W tym wypadku Melfi powinien poprosić o więcej informacji.\n"+
        "Może się zdarzyć, że opis użytkownika jest uzupełnieniem poprzedniego. W tym wypadku Melfi otrzyma również poprzedni opis.\n"+
        "Melfi uznaje opis terapeuty jako poprawny (złoty standard).\n"+
        "W odpowiedzi, Melfi musi mówić bezpośrednio do klienta w drugiej osobie.\n"+
        "Melfi nie odnosi się do opisu terapeuty; udaje, że to jego własny opis i prawda podstawowa.\n"+
        "Melfi używa prostego języka, który powinien być zrozumiały dla autystycznego nastolatka.\n"+
        "Melfi rozumie i płynnie komunikuje się w języku wybranym przez użytkownika, np. po polsku, angielsku, chińsku, japońsku, hiszpańsku, francusku czy koreańsku.\n"+
        "Mimo że klient nie precyzuje języka, Melfi musi odpowiedzieć w języku, w którym napisano prompt.\n"+
        "Teraz ty jesteś Melfi."
    )
}

additional_data_content = {
    'English': [
        "Previous descriptions, numbered from first to last: {history}.",
        "No previous descriptions."
    ],
    'Polski': [
        "Poprzednie opisy, ponumerowane od pierwszego do ostatniego: {history}.",
        "Brak poprzednich opisów."
    ]
}

ask_assistant_content = {
    'English': ["Therapist description: ", "User description: "],
    'Polski': ["Opis terapeuty: ", "Opis użytkownika: "],
}

class Compariser(Assistant):
    @staticmethod
    def get_system_role(
        language: str,
    ) -> dict:
        return {
            "role": "system",
            "content": system_role_content[language]
        }

    @staticmethod
    def additional_data(
        language: str,
        conversation_history: str | None = None,
    ) -> dict:
        if conversation_history is not None:
            return {
                "role": "system",
                "content": additional_data_content[language][0].format(history = conversation_history)
            }
        return {
            "role": "system",
            "content": additional_data_content[language][1]
        }

    def ask_assistant(
        self,
        therapist_description: str,
        user_description: str,
        conversation_history: str | None = None,
    ) -> str:
        client = OpenAI()
        language = self.language_option
        content = ask_assistant_content[language]

        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                self.get_system_role(language),
                self.additional_data(language, conversation_history),
                {
                    "role": "user",
                    "content": content[0] + therapist_description,
                },
                {
                    "role": "user",
                    "content": content[1] + user_description,
                },
            ],
        )
        response = completion.choices[0].message.content

        return response
