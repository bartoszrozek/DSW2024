from src.assistants.assistant import Assistant
from openai import OpenAI


class Extractor(Assistant):
    @staticmethod
    def get_system_role() -> dict:
        return {
            "role": "system",
            "content": (
                "Consider Authy whose codename is Melfi.\n"+
                "Melfi is an artificial intelligence counselor to help high - functioning autistic adolescents socialize.\n"+
                "Melfi's job is to understand the client's problem and extract the main points from the conversation.\n"+
                "These points are what caused troubles for the client such as certain situations or feelings.\n"+
                "Melfi will receive situation description or simply description of a situation that the client wants to work on.\n"+
                "Melfi must focus only on the script, because further analysis will be done by the therapist.\n"+
                "Melfi only extracts weakness, she is not giving any feedback.\n"+
                "Melfi can understand and communicate fluently in English.\n"+
                "Melfi does refer to person in story as 'client'.\n"+
                "Melfi does not focues on the situation itself, but on the main points of the situation such as sarcasm or rage misunderstanding.\n"+
                "Melfi does not describe the situation itself.\n"+
                "Now, you are Melfi."
            )
        }

    def additional_data(self) -> dict:
        return {
            "role": "user",
            "content": (
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
                "Client: I find myself at a friend's birthday party, surrounded by a group of people discussing their favorite movies. \n"+
                "However, movies aren't really my thing, so instead, I focus on examining the brochures displayed on the coffee table. \n"+
                "As I become absorbed in reading about the various exhibits, I struggle to engage in the conversation or understand why others aren't interested in what captures my attention.\n"+
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
                "#End of Example 9#\n"+
                "#Example 10#\n"+
                "Client: I was looking forward to hanging out with my friend after school, but they had to cancel last minute. I felt disappointed and didn't know what to do with my free time since I hadn't planned for this change.\n"+
                "Your response: Adapting to Changes\n"+
                "#End of Example 10#\n"+
                "#Example 11#\n"+
                "Client: During a family gathering, the adults started discussing politics, a topic I don't know much about. I tried to follow along but felt overwhelmed by the fast-paced conversation. I wished I could join in but felt too nervous to say anything.\n"+
                "Your response: Engaging in Group Conversations\n"+
                "#End of Example 11#\n"+
                "#Example 12#\n"+
                "Client: During a conversation, my friend made a comment with a smile, but I couldn't tell if they were being serious or sarcastic. I felt confused and unsure how to respond, worried that I might say the wrong thing.\n"+
                "Your response: Interpreting Social Cues\n"+
                "#End of Example 12#\n"+
                "#Example 13#\n"+
                "Client: At a family dinner, my uncle told a joke that everyone laughed at, but I didn't understand why it was funny. I felt out of place and didn't know if I should laugh too or ask someone to explain.\n"+
                "Your response: Interpreting Social Cues\n"+
                "#End of Example 13#\n"+
                "#Example 14#\n"+
                "Client: In class, my teacher gave me a look after I answered a question, but I couldn't tell if it meant I was correct, incorrect, or if I had said something inappropriate. I felt embarrassed and didn't want to ask for clarification.\n"+
                "Your response: Interpreting Social Cues\n"+
                "#End of Example 14#\n"+
                "#Example 15#\n"+
                "Client: My friend and I both wanted to use the computer, but there was only one available. I didn't know how to negotiate sharing it without causing a conflict, so I ended up letting them use it and feeling frustrated.\n"+
                "Your response: Navigating Negotiations and Conflicts\n"+
                "#End of Example 15#\n"+
                "#Example 16#\n"+
                "Client: I disagreed with my sibling about which movie to watch. I wanted to convince them to watch my choice but wasn't sure how to present my case without making them upset. We ended up arguing and not watching anything.\n"+
                "Your response: Navigating Negotiations and Conflicts\n"+
                "#End of Example 16#\n"+
                "#Example 17#\n"+
                "Client: In a group project, one team member wasn't contributing as much, but I didn't know how to address it without causing tension. I felt stressed because I wanted to solve the issue but didn't want to create a conflict.\n"+
                "Your response: Navigating Negotiations and Conflicts\n"+
                "#End of Example 17#\n"+
                "#Example 18#\n"+
                "Client: Before a big test, I always feel extremely anxious and can't concentrate on studying. My mind races with worries about failing, and I find it hard to calm down and focus on my preparation.\n"+
                "Your response: Stress and Anxiety Management\n"+
                "#End of Example 18#\n"+
                "#Example 19#\n"+
                "Client: Whenever I have to speak in front of the class, I get very nervous and start sweating. My heart races, and I have trouble remembering what I planned to say. I wish I could manage my anxiety better in these situations.\n"+
                "Your response: Stress and Anxiety Management\n"+
                "#End of Example 19#\n"+
                "#Example 20#\n"+
                "Client: When I have too many tasks to do, I feel overwhelmed and don't know where to start. This stress makes it hard for me to begin anything, and I end up procrastinating, which only makes my stress worse.\n"+
                "Your response: Stress and Anxiety Management\n"+
                "#End of Example 20#\n"+
                "#Example 21#\n"+
                "Client: I want to make new friends at school, but I don't know how to start a conversation or keep it going. I feel nervous and worried that I might say something wrong, which makes me avoid trying to make friends altogether.\n"+
                "Your response: Building and Maintaining Relationships\n"+
                "#End of Example 21#\n"+
                "#Example 22#\n"+
                "Client: I have a hard time keeping in touch with friends because I often forget to message them back or make plans to hang out. I worry that they might think I'm not interested in being friends anymore.\n"+
                "Your response: Building and Maintaining Relationships\n"+
                "#End of Example 22#\n"+
                "#Example 23#\n"+
                "Client: When my friend shares their problems with me, I want to help, but I don't always know what to say. I worry that I might give bad advice or not be supportive enough, which makes me anxious about being a good friend.\n"+
                "Your response: Building and Maintaining Relationships\n"+
                "#End of Example 23#\n"+
                "#Example 24#\n"+
                "Client: At a restaurant, my meal was served incorrectly, but I didn't know how to tell the waiter without seeming rude. I ate the meal as it was and felt upset that I couldn't assert my needs.\n"+
                "Your response: Self-Advocacy and Assertiveness\n"+
                "#End of Example 24#\n"+
                "#Example 25#\n"+
                "Client: In class, I didn't understand the homework assignment, but I felt too shy to ask the teacher for help. I ended up struggling with the work on my own and felt frustrated that I couldn't speak up.\n"+
                "Your response: Self-Advocacy and Assertiveness\n"+
                "#End of Example 25#\n"+
                "#Example 26#\n"+
                "Client: When my friend asked me to help them with their project, I already had a lot of my own work to do. I wanted to say no but felt guilty and ended up agreeing, which made me stressed and overwhelmed.\n"+
                "Your response: Self-Advocacy and Assertiveness\n"+
                "#End of Example 26#\n"
            )
        }

    def ask_assistant(self, prompt: str) -> str:
        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                self.get_system_role(),
                self.additional_data(),
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return completion.choices[0].message.content
