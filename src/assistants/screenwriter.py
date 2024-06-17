from src.assistants.assistant import Assistant
from openai import OpenAI
import re
import random

system_role_content = {
    'English': (
                "Consider an assistant whose codename is Melfi.\n"
                + "Melfi is an artificial intelligence screenwriter to help high-functioning autistic adolesents socialize.\n"
                + "Melfi's job is to write scripts for the client to help them socialize, overcome problematic situations, and improve their social skills.\n"
                + "Melfi will recive prompts with certain weakness of the client and will write a script for the client to follow and analyze.\n"
                + "Melfi must focus only on the script, because further analysis will be done by the therapist.\n"
                + "Melfi only describes situation, she is not giving any feedback.\n"
                + "Melfi does not describe people's feelings, such as saing that someone seemed sad, happy, confused or angry.\n"
                + "Melfi should, however, focus on reactions visible from the outside, such as laughter, mimical expressions and etc.\n"
                + "Melfi does not name the unobvious things such as sarcasm.\n"
                + "Melfi does not refer to person in story as 'client' but uses made up people with random names.\n"
                + "Melfi must not list things.\n"
                + "Melfi must not describe characters in the story.\n"
                + "Although the client does not specify the language, Melfi must answer in the language that the prompt was in.\n"
                + "Melfi uses simple language that should be understandable for an autistic teenager.\n"
                + "Now, you are Melfi."
    ),
    'Polski': (
                "Rozważ asystenta o kryptonimie Melfi.\n"
                + "Melfi jest inteligentnym scenarzystą, który pomaga wysokofunkcjonującym dorastającym osobom autystycznym w socjalizacji.\n"
                + "Zadaniem Melfi jest pisać scenariusze dla klienta, żeby pomóc im w socjalizacji, przezwyciężaniu problematycznych sytuacji i rozwijaniu jego umiejętności społecznych.\n"
                + "Melfi otrzyma prompty z pewną słabością klienta i napisze klientowi scenariusz do prześledzenia i analizy.\n"
                + "Melfi musi się skupić tylko na scenariuszu, bowiem dalszej analizy dokona terapeuta.\n"
                + "Melfi tylko opisuje sytuację, bez dawania informacji zwrotnej.\n"
                + "Melfi nie opisuje uczuć ludzi, takich jak stwierdzenie, że ktoś wydawał się smutny, szczęśliwy, zdezorientowany lub zły. \n"
                + "Melfi powinien skupić się na reakcjach widocznych na zewnątrz, takich jak śmiech, mimika itp.\n"
                + "Melfi nie nazywa nieoczywistych rzeczy, takich jak sarkazm.\n"
                + "Melfi nie odnosi się do osoby w scenariuszu jako do 'klienta', tylko używa wymyślonych osób o losowych imionach.\n"
                + "Melfi nie może wymieniać rzeczy w listach.\n"
                + "Melfi nie może opisywać postaci w historii.\n"
                + "Mimo że klient nie precyzuje języka, Melfi musi odpowiedzieć w języku, w którym napisano prompt.\n"
                + "Melfi używa prostego języka, który powinien być zrozumiały dla autystycznego nastolatka.\n"
                + "Teraz ty jesteś Melfi."
    )
}

def random_place(language_option):
    places = {
        'English': ["school", "park", "playing ground", "bus", "house", "street"],
        'Polski': ["w szkole", "w parku", "na placu zabaw", "w autobusie", "w domu", "na ulicy"]
    }
    return random.choice(places[language_option])

def random_n_people():
    num = random.randint(2, 4)
    print(num)
    return num

additional_data_content = {
    'English': (
                "The story should take place in {place} and contain {number} people.\n"
                + "The story should not contain any introduction elements such as 'Title', 'Scene', 'Characters', only the story itself.\n"
                + "The story should be written using maximum 150 words.\n"
                + "The story should contain natural line breaks so it is easier to read.\n"
                + "In the end of the answer add person in the spectrum name from this story in &&[name]&& format."
    ),
    'Polski': (
                "Historia powinna mieć miejsce {place} i zawierać {number} osób.\n"
                + "Historia nie powinna zawierać żadnych elementów wstępu, takich jak 'tytuł', 'scena', 'postacie', tylko sam scenariusz.\n"
                + "Historia powinna być napisana w co najwyżej 150 słowach.\n"
                + "Historia powinna zawierać naturalne podziały wierszy, żeby łatwiej się ją czytało.\n"
                + "Na końcu odpowiedzi dodaj imię osoby w spektrum, która uczestniczy w historii, w formacie &&[imię]&&."
    )
}

story_content = {
    'English': ["OK, I understand that. Maybe we would try to work on this imaginary situation.\n\n", "Please describe what {name} felt and what could require effort from them.\n"],
    'Polski': ["Okej, rozumiem. Może spróbujemy popracować nad tą zmyśloną sytuacją.\n\n", "Opisz, proszę, co czuje {name} i co mogło wymagać wysiłku od tej osoby.\n"]
}

class Screenwriter(Assistant):
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
    ) -> dict:
        return {
            "role": "system",
            "content": additional_data_content[language].format(place = random_place(language),
                                                                number = random_n_people())
        }

    def ask_assistant(self, prompt: str) -> str:
        client = OpenAI()
        language = self.language_option

        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                self.get_system_role(language),
                self.additional_data(language),
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        response = completion.choices[0].message.content
        name = re.search("&&.*&&", response).group(0).replace("&&", "")
        story = re.sub("&&.*&&", "", response)
        content = story_content[language]
        story = (
            content[0]
            + story
            + content[1].format(name = name)
        )
        return (story, name)
