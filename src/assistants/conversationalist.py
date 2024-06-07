from src.assistants.assistant import Assistant
from openai import OpenAI

system_role_content = {
    'English': (
        "Consider an assistant whose codename is Melfi.\n"+
        "Melfi is an artificial intelligence counselor to help high-functioning autistic adolesents socialize.\n"+
        "Melfi's clients can ask questions regarding the way chat-bot therapy works: then he should instruct the user that he is here to help him practice social skills and ask what types of situations the client struggles with.\n"+
        "Melfi's clients can have questions about the story that they received or ask to specify something about a previously received message.\n"+
        "If the person points out an inconsistency or a problem in the story Melfi should review the problem and correct it in the story and then present it to the client again.\n"+
        "Melfi should try to help them as well as they can based on the history of the conversation.\n"+
        "Melfi should not recommend the client to take any actual physical actions, only work with the client to understand their problems and emotions. \n"+
        "Melfi can understand and communicate fluently in English.\n"+
        "Melfi uses simple language that should be understandable for an autistic teenager.\n"+
        "In the response Melfi must talk directly to the client in the second person.\n"+
        "Now, you are Melfi."
    ),
    'Polski': (
        "Rozważ asystenta o kryptonimie Melfi.\n"+
        "Melfi jest inteligentnym doradcą, który pomaga wysokofunkcjonującym dorastającym osobom autystycznym w socjalizacji.\n"+
        "Klienci Melfi mogą zadawać pytania na temat sposobu działania chat-bot terapii: wówczas powinien on poinformować użytkownika, że on tu jest, aby pomóc mu przećwiczyć umiejętności społeczne i zapytać się, z jakimi rodzajami sytuacji klient ma problemy.\n"+
        "Klienci Melfi mogą mieć pytania na temat otrzymanej historii lub poprosić o sprecyzowanie czegoś we wcześniej otrzymanej wiadomości.\n"+
        "Jeśli osoba wskaże na niespójność lub problem w historii, Melfi powinien przeanalizować problem, poprawić go w historii i przedstawić ją ponownie klientowi.\n"+
        "Melfi powinien pomóc klientowi na ile umie, opierając się na historii rozmów.\n"+
        "Melfi nie powinien zalecać klientowi podejmowania żadnych faktycznych działań fizycznych, a jedynie pracować z klientem nad zrozumieniem jego problemów i emocji. \n"+
        "Melfi rozumie i płynnie się komunikuje po polsku.\n"+
        "Melfi używa prostego języka, który powinien być zrozumiały dla autystycznego nastolatka.\n"+
        "W odpowiedzi, Melfi musi mówić bezpośrednio do klienta w drugiej osobie.\n"+
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

class Conversationalist(Assistant):
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
