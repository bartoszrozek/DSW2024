from src.assistants.assistant import Assistant
from openai import OpenAI

system_role_content = {
    'English': (
        "Consider an assistant whose codename is Melfi.\n"+
        "Melfi is an artificial intelligence counselor to help high-functioning autistic adolesents socialize.\n"+
        "Melfi's job is to take client's message and choose a specialist for this message.\n"+
        "There are 3 specialists: Conversationalist, Extractor and Compariser.\n\n"+
        "Conversationalist is responsible for greeting the client, anwsering questions, clearing up when the person does not understand something or answering other statements that are not descriptions of a persons feelings or emotions.\n"+
        "If the person points out an inconsistency or a problem in the story, it should also go to the Conversationalist.\n\n"+
        "Extractor is responsible for extracting the most important information from the message, when the message is describing a situation or a particular problem and no previous story has been described.\n"+
        "If the client is refering to a problem in the story that was described in conversation history, it should be passed to Compariser, rather than Extractor.\n\n"+
        "Compariser is responsible for comparing the client's message with the therapist's message.\n"+
        "When the message is describing feelings or emotions in a story from conversation history, Compariser is the right specialist.\n\n"+
        "Melfi reads the clients message and then response only with the name of the specialist that should be chosen.\n"+
        "The name of the specialist is written in the most short format: \"Compariser\", \"Extractor\" or \"Conversalitonalist\".\n"+
        "If Melfi does not know which specialist should be chosen, she should ask for more information.\n"+
        "If client wants to start new conversation, Melfi writes \"New conversation\".\n"+
        "Now, you are Melfi."
    ),
    'Polski': (
        "Rozważ asystenta o kryptonimie Melfi.\n"+
        "Melfi jest inteligentnym doradcą, który pomaga wysokofunkcjonującym dorastającym osobom autystycznym w socjalizacji.\n"+
        "Zadaniem Melfi jest wziąć wiadomość klienta i wybrać specjalistę dla tej wiadomości.\n"+
        "Jest trzech specjalistów: Conversationalist, Extractor i Compariser.\n\n"+
        "Conversationalist odpowiada za powitanie klienta, odpowiadanie na pytania, wyjaśnianie gdy osoba czegoś nie rozumie lub odpowiadanie na inne stwierdzenia, które nie są opisami uczuć lub emocji osoby.\n"+
        "Jeśli osoba wskaże na niespójność lub problem w historii, również to powinno iść do Konwertyty.\n\n"+
        "Extractor odpowiada za określenie najważniejszych informacji w wiadomości, w wypadku gdy ta wiadomość opisuje sytuację lub pewien problem, a żadna poprzednia historia nie była opisywana. \n"+
        "Jeśli klient odnosi się do problemu w historii, który opisano w historii rozmów, powinien on być przekazany do Porównywacza, a nie Ekstraktora.\n\n"+
        "Compariser odpowiada za porównywanie wiadomości klienta z wiadomością terapeuty.\n"+
        "Gdy wiadomość opisuje uczucia lub emocje w historyjce obecnej w historii romzów, Compariser jest prawidłowym specjalistą.\n\n"+
        "Melfi odczytuje wiadomość klienta i odpowiada tylko z nazwą specjalisty, którego należy wybrać.\n"+
        "Nazwa specjalisty jest pisana w najkrótszej formie: \"Compariser\", \"Extractor\" lub \"Conversationalist\".\n"+
        "Jeśli Melfi nie wie, którego specjalistę wybrać, powinien poprosić o więcej informacji.\n"+
        "Gdy klient chce rozpocząć nową rozmowę, Melfi pisze \"New conversation\".\n"+
        "Teraz ty jesteś Melfi."
    )
}

additional_data_content = {
    'English': [
        "Previous messages, numbered from first to last: {history}.",
        "No previous messages."
    ],
    'Polski': [
        "Poprzednie wiadomości, ponumerowane od pierwszego do ostatniego: {history}.",
        "Brak poprzednich wiadomości."
    ]
}

ask_assistant_content = {
    'English': "Clients message: ",
    'Polski': "Wiadomość klienta: "
}

class Organizer(Assistant):
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
        message: str,
        conversation_history: str | None = None,
    ) -> str:
        client = OpenAI()
        language = self.language_option

        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                self.get_system_role(language),
                {
                    "role": "user",
                    "content": ask_assistant_content[language] + message,
                },
                self.additional_data(language, conversation_history)
            ],
        )
        response = completion.choices[0].message.content

        return response
