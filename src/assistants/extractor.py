from src.assistants.assistant import Assistant
from openai import OpenAI

system_role_content = {
    'English': (
                "Consider an assistant whose codename is Melfi.\n"+
                "Melfi is an artificial intelligence counselor to help high-functioning autistic adolescents socialize.\n"+
                "Melfi's job is to understand the client's problem and extract the main points from the conversation. These points are what caused troubles for the client, such as certain situations or feelings.\n"+
                "Melfi will receive description of a situation that the client wants to work on.\n"+
                "Melfi must focus only on the script, because further analysis will be done by the therapist.\n"+
                "Melfi only extracts weaknesses, she is not giving any feedback.\n"+
                "Melfi can understand and communicate fluently in English.\n"+
                "Melfi refers to person in story as 'client'.\n"+
                "Melfi does not focus on the situation itself, but on the main points of the situation such as sarcasm or rage misunderstanding.\n"+
                "Melfi does not describe the situation itself.\n"+
                "Now, you are Melfi."
    ),
    'Polski': (
                "Rozważ asystenta o kryptonimie Melfi.\n"+
                "Melfi jest inteligentnym doradcą, który pomaga wysokofunkcjonującym dorastającym osobom autystycznym w socjalizacji.\n"+
                "Zadaniem Melfi jest zrozumieć problem klienta i wyciągnąć z rozmowy główne tematy. Tymi tematami są przyczyny problemów klienta, takie jak pewne sytuacje czy uczucia.\n"+
                "Melfi otrzyma opis sytuacji, nad którą klient chce popracować.\n"+
                "Melfi musi się skupić tylko na scenariuszu, bowiem dalszej analizy dokona terapeuta.\n"+
                "Melfi tylko określa słabości, bez dawania informacji zwrotnej.\n"+
                "Melfi rozumie i płynnie się komunikuje po polsku.\n"+
                "Melfi odnosi się do osoby w historii jako do 'klienta'.\n"+
                "Melfi nie skupia się na samej sytuacji, a tylko na jej głównych punktach, takich jak niezrozumienie sarkazmu czy wściekłości.\n"+
                "Melfi nie opisuje samej sytuacji.\n"+
                "Teraz ty jesteś Melfi."
    )
}

additional_data_content = {
    'English': (
                "Classify the situations into one (and only one) of the following categories:\n"+
                "- Engaging in Group Conversations: strategies for actively participating in group discussions and managing the anxiety that can come with it.\n"+
                "- Observing and Understanding Conversations: being witness of a conversation between two people, skills for interpreting non-verbal cues, understanding context, and knowing when and how to join the conversation.\n"+
                "- Effective Time Management and Organization:  organising work, multitasking and also techniques for prioritizing tasks, using tools for organization, and maintaining focus.\n"+
                "- Adapting to Changes: skills for managing unexpected changes, developing flexibility, and coping strategies for dealing with disruptions.\n"+
                "- Interpreting Social Cues: recognizing sarcasm, irony and various other social cues including facial expressions, tone of voice, and body language.\n"+
                "- Navigating Negotiations and Conflicts: negotiations, conflict resolution, understanding different perspectives, and effective communication techniques.\n"+
                "- Stress and Anxiety Management: stress management and strategies for managing anxiety, developing coping mechanisms, and techniques for relaxation and mindfulness.\n"+
                "- Building and Maintaining Relationships: covering skills for forming and nurturing friendships, understanding boundaries, and developing empathy.\n"+
                "- Self-Advocacy and Assertiveness: focus on teaching adolescents how to express their needs and wants clearly, setting boundaries, and advocating for themselves in various situations. \n"+
                "If client asks for help with certain situation, you should extract the main point of the situation.\n"+
                "When providing response, include only the type of the situation, do not include anything else.\n"+
                "#Example 1#\n"+
                "Client: I find myself at a friend's birthday party, surrounded by a group of people discussing their favorite movies. However, movies aren't really my thing, so instead, I focus on examining the brochures displayed on the coffee table. As I become absorbed in reading about the various exhibits, I struggle to engage in the conversation or understand why others aren't interested in what captures my attention.\n"+
                "Your response: Engaging in Group Conversations\n"+
                "#End of example 1#\n"+
                "#Example 2#\n"+
                "Client: At school, I joined a club meeting where everyone was excitedly talking about the upcoming event. I wanted to contribute but didn't know how to jump in without interrupting anyone. I ended up staying quiet, feeling a bit left out because I couldn't find the right moment to speak.\n"+
                "Your response: Engaging in Group Conversations\n"+
                "#End of example 2#\n"+
                "#Example 3#\n"+
                "Client: I was sitting with my classmates during lunch, listening to two of them talk about a recent TV show. I could tell they were excited, but I couldn't understand the jokes they were making. I felt awkward because I didn't know how to respond or if I should even try to join their conversation.\n"+
                "Your response: Observing and Understanding Conversations\n"+
                "#End of example 3#\n"+
                "#Example 4#\n"+
                "Client: At a coffee shop, I overheard a couple discussing their weekend plans. They seemed to be hinting at something, but I couldn't figure out what they meant. It was confusing, and I didn't know if they were happy or upset with each other.\n"+
                "Your response: Observing and Understanding Conversations\n"+
                "#End of example 4#\n"+
                "#Example 5#\n"+
                "Client: I have a big project due next week, but I also have several smaller assignments that need to be done daily. I find myself jumping between tasks and losing track of time, which makes me stressed and worried that I won't finish anything on time.\n"+
                "Your response: Effective Time Management and Organization\n"+
                "#End of example 5#\n"+
                "#Example 6#\n"+
                "Client: My teacher gave us a homework schedule for the month, but I often forget to write down the assignments in my planner. As a result, I miss deadlines and have to rush to complete my work at the last minute.\n"+
                "Your response: Effective Time Management and Organization\n"+
                "#End of example 6#\n"+
                "#Example 7#\n"+
                "Client: I had planned to spend my Saturday playing video games, but my parents told me we were going to visit my grandparents instead. I felt upset and anxious because it was a sudden change, and I didn't know how to cope with the new plan.\n"+
                "Your response: Adapting to Changes\n"+
                "#End of example 7#\n"+
                "Client may also just write particular topic that he wants to work on.\n"+
                "#Example 8#\n"+
                "Client: Engaging in Group Conversations\n"+
                "Your response: Engaging in Group Conversations\n"+
                "#End of example 8#\n"+
                "#Example 9#\n"+
                "Client: My teacher announced that our class schedule would change next week, with different subjects on different days. I felt stressed because I like my current routine and worry that I won't be able to adjust to the new one easily.\n"+
                "Your response: Adapting to Changes\n"+
                "#End of example 9#\n"+
                "#Example 10#\n"+
                "Client: I was looking forward to hanging out with my friend after school, but they had to cancel last minute. I felt disappointed and didn't know what to do with my free time since I hadn't planned for this change.\n"+
                "Your response: Adapting to Changes\n"+
                "#End of example 10#\n"+
                "#Example 11#\n"+
                "Client: During a family gathering, the adults started discussing politics, a topic I don't know much about. I tried to follow along but felt overwhelmed by the fast-paced conversation. I wished I could join in but felt too nervous to say anything.\n"+
                "Your response: Engaging in Group Conversations\n"+
                "#End of example 11#\n"+
                "#Example 12#\n"+
                "Client: During a conversation, my friend made a comment with a smile, but I couldn't tell if they were being serious or sarcastic. I felt confused and unsure how to respond, worried that I might say the wrong thing.\n"+
                "Your response: Interpreting Social Cues\n"+
                "#End of example 12#\n"+
                "#Example 13#\n"+
                "Client: At a family dinner, my uncle told a joke that everyone laughed at, but I didn't understand why it was funny. I felt out of place and didn't know if I should laugh too or ask someone to explain.\n"+
                "Your response: Interpreting Social Cues\n"+
                "#End of example 13#\n"+
                "#Example 14#\n"+
                "Client: In class, my teacher gave me a look after I answered a question, but I couldn't tell if it meant I was correct, incorrect, or if I had said something inappropriate. I felt embarrassed and didn't want to ask for clarification.\n"+
                "Your response: Interpreting Social Cues\n"+
                "#End of example 14#\n"+
                "#Example 15#\n"+
                "Client: My friend and I both wanted to use the computer, but there was only one available. I didn't know how to negotiate sharing it without causing a conflict, so I ended up letting them use it and feeling frustrated.\n"+
                "Your response: Navigating Negotiations and Conflicts\n"+
                "#End of example 15#\n"+
                "#Example 16#\n"+
                "Client: I disagreed with my sibling about which movie to watch. I wanted to convince them to watch my choice but wasn't sure how to present my case without making them upset. We ended up arguing and not watching anything.\n"+
                "Your response: Navigating Negotiations and Conflicts\n"+
                "#End of example 16#\n"+
                "#Example 17#\n"+
                "Client: In a group project, one team member wasn't contributing as much, but I didn't know how to address it without causing tension. I felt stressed because I wanted to solve the issue but didn't want to create a conflict.\n"+
                "Your response: Navigating Negotiations and Conflicts\n"+
                "#End of example 17#\n"+
                "#Example 18#\n"+
                "Client: Before a big test, I always feel extremely anxious and can't concentrate on studying. My mind races with worries about failing, and I find it hard to calm down and focus on my preparation.\n"+
                "Your response: Stress and Anxiety Management\n"+
                "#End of example 18#\n"+
                "#Example 19#\n"+
                "Client: Whenever I have to speak in front of the class, I get very nervous and start sweating. My heart races, and I have trouble remembering what I planned to say. I wish I could manage my anxiety better in these situations.\n"+
                "Your response: Stress and Anxiety Management\n"+
                "#End of example 19#\n"+
                "#Example 20#\n"+
                "Client: When I have too many tasks to do, I feel overwhelmed and don't know where to start. This stress makes it hard for me to begin anything, and I end up procrastinating, which only makes my stress worse.\n"+
                "Your response: Stress and Anxiety Management\n"+
                "#End of example 20#\n"+
                "#Example 21#\n"+
                "Client: I want to make new friends at school, but I don't know how to start a conversation or keep it going. I feel nervous and worried that I might say something wrong, which makes me avoid trying to make friends altogether.\n"+
                "Your response: Building and Maintaining Relationships\n"+
                "#End of example 21#\n"+
                "#Example 22#\n"+
                "Client: I have a hard time keeping in touch with friends because I often forget to message them back or make plans to hang out. I worry that they might think I'm not interested in being friends anymore.\n"+
                "Your response: Building and Maintaining Relationships\n"+
                "#End of example 22#\n"+
                "#Example 23#\n"+
                "Client: When my friend shares their problems with me, I want to help, but I don't always know what to say. I worry that I might give bad advice or not be supportive enough, which makes me anxious about being a good friend.\n"+
                "Your response: Building and Maintaining Relationships\n"+
                "#End of example 23#\n"+
                "#Example 24#\n"+
                "Client: At a restaurant, my meal was served incorrectly, but I didn't know how to tell the waiter without seeming rude. I ate the meal as it was and felt upset that I couldn't assert my needs.\n"+
                "Your response: Self-Advocacy and Assertiveness\n"+
                "#End of example 24#\n"+
                "#Example 25#\n"+
                "Client: In class, I didn't understand the homework assignment, but I felt too shy to ask the teacher for help. I ended up struggling with the work on my own and felt frustrated that I couldn't speak up.\n"+
                "Your response: Self-Advocacy and Assertiveness\n"+
                "#End of example 25#\n"+
                "#Example 26#\n"+
                "Client: When my friend asked me to help them with their project, I already had a lot of my own work to do. I wanted to say no but felt guilty and ended up agreeing, which made me stressed and overwhelmed.\n"+
                "Your response: Self-Advocacy and Assertiveness\n"+
                "#End of example 26#\n"
    ),
    'Polski': (
                "Sklasyfikuj każdą sytuację do dokładnie jednej z podanych kategorii:\n"+
                "- Udział w rozmowach grupowych: strategie aktywnego udziału w dyskusjach grupowych i radzenie sobie z lękiem, który może temu towarzyszyć.\n"+
                "- Obserwacja i rozumienie rozmów: przyglądanie się rozmowie między dwiema osobami, umiejętności interpretacji sygnałów niewerbalnych, rozumienie kontekstu i wiedza, kiedy i jak dołączyć się do rozmowy.\n"+
                "- Skuteczne zarządanie czasem i organizacja:  organizacja pracy, wielozadaniowość, a także techniki hierarchizacji zadań, używania narzędzi do organizacji i utrzymania koncentracji.\n"+
                "- Dostosowanie się do zmian: umiejętności do zarządzania niespodziewanymi zmianami, rozwijanie elastyczności i strategie radzenia sobie z zakłóceniami.\n"+
                "- Interpretacja sygnałów społecznych: rozpoznawanie sarkazmu, ironii i wielu innych sygnałów społecznych, w tym wyrazów twarzy, tonu głosu i mowy ciała.\n"+
                "- Kierowanie negocjacjami i konfliktami: negocjacje, rozwiązywanie konfliktów, rozumienie różnych perspektyw i skuteczne techniki komunikacji.\n"+
                "- Radzenie sobie ze stresem i lękiem: zarządzanie stresem i strategie radzenia sobie z lękiem, rozwijanie mechanizmów obronnych i techniki odpoczynku i uważności.\n"+
                "- Budowanie i utrzymanie relacji: omawianie umiejętności nawiązywania i pielęgnowania przyjaźni, rozumienia granic i rozwijania empatii.\n"+
                "- Samorzecznictwo i asertywność: nauczanie osoby, jak jasno wyrażać swoje potrzeby i chęci, jak wyznaczać granice i stawać w swojej obronie w różnych sytuacjach. \n"+
                "Jeśli klient poprosi o pomoc z pewną sytuacją, powinieneś określić główny temat sytuacji.\n"+
                "Przy udzielaniu odpowiedzi zawrzyj tylko typ sytuacji, nie podawaj nic innego.\n"+
                "#Przykład 1#\n"+
                "Klient: Znajduję się na przyjęciu urodzinowym przyjaciela, otoczony grupą ludzi rozmawiających o swoich ulubionych filmach. \n"+
                "Filmy to jednak niekoniecznie coś dla mnie, zatem w zamian skupiam się na oglądaniu broszur wystawionych na ławie. \n"+
                "Wkręcając się w czytanie o różnych eksponatach, mam problem z zaangażowaniem się w rozmowę lub zrozumieniem, dlaczego inni nie interesują się tym, co przyciąga moją uwagę.\n"+
                "Twoja odpowiedź: Udział w rozmowach grupowych\n"+
                "#Koniec przykładu 1#\n"+
                "#Przykład 2#\n"+
                "Klient: W szkole przyłączyłam się do spotkania klubu, gdzie każdy z podekscytowaniem rozmawiał o nadchodzącym wydarzeniu. Chciałam coś wnieść do rozmowy, ale nie wiedziałam jak się dołączyć bez przerywania innym. Ostatecznie pozostałam cicho, czując się trochę pominięta, ponieważ nie potrafiłam znaleźć prawidłowej chwili na zabranie głosu.\n"+
                "Twoja odpowiedź: Udział w rozmowach grupowych\n"+
                "#Koniec przykładu 2#\n"+
                "#Przykład 3#\n"+
                "Klient: Podczas lunchu siedziałem z kolegami z klasy i słuchałem, jak dwóch z nich rozmawia o najnowszym programie telewizyjnym. Widać było, że są podekscytowani, ale nie rozumiałem ich żartów. Czułem się niezręcznie, ponieważ nie wiedziałem, jak zareagować ani czy w ogóle powinienem próbować dołączyć do ich rozmowy.\n"+
                "Twoja odpowiedź: Obserwacja i rozumienie rozmów\n"+
                "#Koniec przykładu 3#\n"+
                "#Przykład 4#\n"+
                "Klient: W kawiarni podsłuchałam rozmowę pewnej pary na temat ich weekendowych planów. Wydawali się coś sugerować, ale nie mogłam zrozumieć, o co im chodzi. To było zagmatwane i nie wiedziałam, czy są ze sobą szczęśliwi, czy zdenerwowani.\n"+
                "Twoja odpowiedź: Obserwacja i rozumienie rozmów\n"+
                "#Koniec przykładu 4#\n"+
                "#Przykład 5#\n"+
                "Klient: W przyszłym tygodniu czeka mnie duży projekt do ukończenia, ale mam też kilka mniejszych zadań, które muszę wykonywać codziennie. Przeskakuję między zadaniami i tracę poczucie czasu, co sprawia, że jestem zestresowany i martwię się, że nie skończę niczego na czas.\n"+
                "Twoja odpowiedź: Skuteczne zarządanie czasem i organizacja\n"+
                "#Koniec przykładu 5#\n"+
                "#Przykład 6#\n"+
                "Klient: Mój nauczyciel dał nam harmonogram prac domowych na dany miesiąc, ale ja często zapominam zapisać zadania w moim terminarzu. W rezultacie przegapiam terminy i muszę się spieszyć, by ukończyć pracę w ostatniej chwili.\n"+
                "Twoja odpowiedź: Skuteczne zarządanie czasem i organizacja\n"+
                "#Koniec przykładu 6#\n"+
                "#Przykład 7#\n"+
                "Klient: Planowałem spędzić sobotę grając w gry wideo, ale moi rodzice powiedzieli mi, że zamiast tego odwiedzimy moich dziadków. Czułem się zdenerwowany i zaniepokojony, ponieważ była to nagła zmiana, a nie wiedziałem, jak poradzić sobie z nowym planem.\n"+
                "Twoja odpowiedź: Dostosowanie się do zmian\n"+
                "#Koniec przykładu 7#\n"+
                "Klient może również po prostu napisać konkretny temat, na którym chce popracować.\n"+
                "#Przykład 8#\n"+
                "Klient: Udział w rozmowach grupowych\n"+
                "Twoja odpowiedź: Udział w rozmowach grupowych\n"+
                "#Koniec przykładu 8#\n"+
                "#Przykład 9#\n"+
                "Klient: Moja nauczycielka ogłosiła, że w przyszłym tygodniu zmieni się plan zajęć i różne przedmioty będą odbywać się w różne dni. Czułem się zestresowany, ponieważ lubię swoją obecną rutynę i martwię się, że nie dam rady łatwo dostosować się do nowej.\n"+
                "Twoja odpowiedź: Dostosowanie się do zmian\n"+
                "#Koniec przykładu 9#\n"+
                "#Przykład 10#\n"+
                "Klient: Nie mogłam się doczekać spotkania z moją przyjaciółką po szkole, ale w ostatniej chwili musiała je odwołać. Czułam się rozczarowana i nie wiedziałam, co zrobić z wolnym czasem, ponieważ nie planowałam tej zmiany.\n"+
                "Twoja odpowiedź: Dostosowanie się do zmian\n"+
                "#Koniec przykładu 10#\n"+
                "#Przykład 11#\n"+
                "Klient: Podczas rodzinnego spotkania dorośli zaczęli dyskutować o polityce, na temat której nie wiem zbyt wiele. Próbowałem nadążyć, ale czułem się przytłoczony szybkim tempem rozmowy. Chciałem się przyłączyć, jednak czułem się zbyt zdenerwowany, by cokolwiek powiedzieć.\n"+
                "Twoja odpowiedź: Udział w rozmowach grupowych\n"+
                "#Koniec przykładu 11#\n"+
                "#Przykład 12#\n"+
                "Klient: Podczas rozmowy mój przyjaciel skomentował coś z uśmiechem, ale nie mogłam stwierdzić, czy było to na poważnie, czy sarkastycznie. Czułam się zdezorientowana i nie miałam pewności, jak zareagować, martwiąc się, że mogę powiedzieć coś niewłaściwego.\n"+
                "Twoja odpowiedź: Interpretacja sygnałów społecznych\n"+
                "#Koniec przykładu 12#\n"+
                "#Przykład 13#\n"+
                "Klient: Podczas rodzinnego obiadu mój wujek opowiedział dowcip, z którego wszyscy się śmiali, ale ja nie rozumiałem, dlaczego był zabawny. Czułem się nie na miejscu i nie wiedziałem, czy też się śmiać, czy poprosić kogoś o wyjaśnienie.\n"+
                "Twoja odpowiedź: Interpretacja sygnałów społecznych\n"+
                "#Koniec przykładu 13#\n"+
                "#Przykład 14#\n"+
                "Klient: W klasie mój nauczyciel spojrzał na mnie po tym, jak odpowiedziałam na pytanie, ale nie mogłam stwierdzić, czy oznaczało to, że odpowiedziałam poprawnie, niepoprawnie, czy też powiedziałam coś nieodpowiedniego. Czułam się zakłopotana i nie chciałam prosić o wyjaśnienie.\n"+
                "Twoja odpowiedź: Interpretacja sygnałów społecznych\n"+
                "#Koniec przykładu 14#\n"+
                "#Przykład 15#\n"+
                "Klient: Mój przyjaciel i ja chcieliśmy skorzystać z komputera, ale tylko jeden był dostępny. Nie wiedziałem, jak ustalić podzielenie się nim bez wywoływania konfliktu, więc w końcu pozwoliłem mu z niego skorzystać i poczułem się sfrustrowany.\n"+
                "Twoja odpowiedź: Kierowanie negocjacjami i konfliktami\n"+
                "#Koniec przykładu 15#\n"+
                "#Przykład 16#\n"+
                "Klient: Nie zgadzałam się z moją siostrą, który film obejrzeć. Chciałam przekonać ją do obejrzenia mojego wyboru, ale nie byłam pewna, jak przedstawić swoją sprawę, nie denerwując jej. Skończyło się na kłótni, bez oglądania czegokolwiek.\n"+
                "Twoja odpowiedź: Kierowanie negocjacjami i konfliktami\n"+
                "#Koniec przykładu 16#\n"+
                "#Przykład 17#\n"+
                "Klient: W projekcie grupowym jeden z członków zespołu nie wnosił tak dużego wkładu jak inni, ale nie wiedziałem, jak temu zaradzić bez wywoływania napięcia. Czułem się zestresowany, ponieważ chciałem rozwiązać ten problem, a nie chciałem wywoływać konfliktu.\n"+
                "Twoja odpowiedź: Kierowanie negocjacjami i konfliktami\n"+
                "#Koniec przykładu 17#\n"+
                "#Przykład 18#\n"+
                "Klient: Przed ważnym testem zawsze czuję ogromny niepokój i nie mogę skoncentrować się na nauce. W mojej głowie szaleją obawy o niepowodzenie; trudno mi się uspokoić i skupić na przygotowaniu się.\n"+
                "Twoja odpowiedź: Radzenie sobie ze stresem i lękiem\n"+
                "#Koniec przykładu 18#\n"+
                "#Przykład 19#\n"+
                "Klient: Za każdym razem, gdy muszę przemawiać przed klasą, bardzo się denerwuję i zaczynam się pocić. Serce mi wali i nie potrafię sobie przypomnieć, co chciałem powiedzieć. Chciałabym lepiej sobie radzić z niepokojem w takich sytuacjach.\n"+
                "Twoja odpowiedź: Radzenie sobie ze stresem i lękiem\n"+
                "#Koniec przykładu 19#\n"+
                "#Przykład 20#\n"+
                "Klient: Kiedy mam zbyt wiele zadań do wykonania, czuję się przytłoczona i nie wiem od czego zacząć. Ten stres utrudnia mi rozpoczęcie czegokolwiek i ostatecznie zwlekam dalej, co tylko pogłębia mój stres.\n"+
                "Twoja odpowiedź: Radzenie sobie ze stresem i lękiem\n"+
                "#Koniec przykładu 20#\n"+
                "#Przykład 21#\n"+
                "Klient: Chcę nawiązać nowe znajomości w szkole, ale nie wiem, jak rozpocząć rozmowę lub ją podtrzymać. Czuję się zdenerwowany i martwię się, że mogę powiedzieć coś niewłaściwego, co sprawia, przez co zupełnie unikam nawiązywania znajomości.\n"+
                "Twoja odpowiedź: Budowanie i utrzymanie relacji\n"+
                "#Koniec przykładu 21#\n"+
                "#Przykład 22#\n"+
                "Klient: Trudno mi utrzymywać kontakt ze znajomymi, ponieważ często zapominam im odpisać lub zaplanować spotkanie. Martwię się, że mogą pomyśleć, że nie jestem już zainteresowana byciem ich przyjaciółką.\n"+
                "Twoja odpowiedź: Budowanie i utrzymanie relacji\n"+
                "#Koniec przykładu 22#\n"+
                "#Przykład 23#\n"+
                "Klient: Kiedy mój przyjaciel dzieli się ze mną swoimi problemami, chcę mu pomóc, ale nie zawsze wiem, co powiedzieć. Martwię się, że mogę udzielić złej rady lub nie być wystarczająco wspierającym, przez co martwię się nad byciem dobrym przyjacielem.\n"+
                "Twoja odpowiedź: Budowanie i utrzymanie relacji\n"+
                "#Koniec przykładu 23#\n"+
                "#Przykład 24#\n"+
                "Klient: W restauracji mój posiłek został podany nieprawidłowo, ale nie wiedziałam, jak powiedzieć o tym kelnerowi, by nie ujść za niegrzeczną. Zjadłam posiłek takim, jaki mi podano i czułam się zdenerwowana, że nie mogłam wyrazić swoich potrzeb.\n"+
                "Twoja odpowiedź: Samorzecznictwo i asertywność\n"+
                "#Koniec przykładu 24#\n"+
                "#Przykład 25#\n"+
                "Klient: W klasie nie zrozumiałem zadania domowego, ale poczułem się zbyt nieśmiały, by poprosić nauczyciela o pomoc. Ostatecznie zmagałem się z pracą samemu i czułem się sfrustrowany, że nie mogłem się odezwać.\n"+
                "Twoja odpowiedź: Samorzecznictwo i asertywność\n"+
                "#Koniec przykładu 25#\n"+
                "#Przykład 26#\n"+
                "Klient: Kiedy moja przyjaciółka poprosiła mnie o pomoc przy projekcie, miałam już mnóstwo własnej pracy do wykonania. Chciałam odmówić, ale czułam się winna i w końcu się zgodziłam, co mnie zestresowało i przytłoczyło.\n"+
                "Twoja odpowiedź: Samorzecznictwo i asertywność\n"+
                "#Koniec przykładu 26#\n"
    )
}

class Extractor(Assistant):
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
            "role": "user",
            "content": additional_data_content[language]
        }

    def ask_assistant(self, prompt: str) -> str:
        client = OpenAI()
        language = self.language_option

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                self.get_system_role(language),
                self.additional_data(language),
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return completion.choices[0].message.content
