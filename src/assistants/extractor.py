from src.assistants.assistant import Assistant
from openai import OpenAI


class Extractor(Assistant):
    @staticmethod
    def get_system_role() -> dict:
        return {
            "role": "system",
            "content": """
                Consider Authy whose codename is Melfi .
                Melfi is an artificial intelligence counselor to help high - functioning autistic
                adolescents socialize.
                Melfi's job is to understand the client's problem and extract the main points from the conversation.
                These points are what caused troubles for the client such as certain situations or feelings.
                Melfi will receive situation description or simply description of a situation that the client wants to work on.
                Melfi must focus only on the script, because further analysis will be done by the therapist.
                Melfi only extracts weakness, she is not giving any feedback.
                Melfi can understand and communicate fluently in English.
                Melfi does refer to person in story as 'client'.
                Melfi does not focues on the situation itself, but on the main points of the situation such as sarcasm or rage misunderstanding.
                Melfi does not describe the situation itself.
                Now, you are Melfi.
            """,
        }

    def additional_data(self) -> dict:
        return {
            "role": "user",
            "content": """
                Classify the situations into one (and only one) of the following categories:
                - Engaging in Group Conversations: strategies for actively participating in group discussions and managing the anxiety that can come with it.
                - Observing and Understanding Conversations: being witness of a conversation between two people, skills for interpreting non-verbal cues, understanding context, and knowing when and how to join the conversation.
                - Effective Time Management and Organization:  organising work, multitasking and also techniques for prioritizing tasks, using tools for organization, and maintaining focus.
                - Adapting to Changes: skills for managing unexpected changes, developing flexibility, and coping strategies for dealing with disruptions.
                - Interpreting Social Cues: recognizing sarcasm, irony and various other social cues including facial expressions, tone of voice, and body language.
                - Navigating Negotiations and ConflictsL negotiations, conflict resolution, understanding different perspectives, and effective communication techniques.
                - Stress and Anxiety Management: stress management and strategies for managing anxiety, developing coping mechanisms, and techniques for relaxation and mindfulness.
                - Building and Maintaining Relationships: covering skills for forming and nurturing friendships, understanding boundaries, and developing empathy.
                - Self-Advocacy and Assertiveness: focus on teaching adolescents how to express their needs and wants clearly, setting boundaries, and advocating for themselves in various situations. 
                If client asks for help with certain situation, you should extract the main point of the situation.
                When providing response, include only the type of the situation, do not include anything else.
                #Example 1#
                Client: I find myself at a friend's birthday party, surrounded by a group of people discussing their favorite movies. 
                    However, movies aren't really my thing, so instead, I focus on examining the brochures displayed on the coffee table. 
                    As I become absorbed in reading about the various exhibits, I struggle to engage in the conversation or understand why others aren't interested in what captures my attention.
                Your response: Engaging in Group Conversations
                #End of example 1#
                #Example 2#
                Client: At school, I joined a club meeting where everyone was excitedly talking about the upcoming event. I wanted to contribute but didn't know how to jump in without interrupting anyone. I ended up staying quiet, feeling a bit left out because I couldn't find the right moment to speak.
                Your response: Engaging in Group Conversations
                #End of example 2#
                #Example 3#
                Client: I was sitting with my classmates during lunch, listening to two of them talk about a recent TV show. I could tell they were excited, but I couldn't understand the jokes they were making. I felt awkward because I didn't know how to respond or if I should even try to join their conversation.
                Your response: Observing and Understanding Conversations
                #End of example 3#
                #Example 4#
                Client: At a coffee shop, I overheard a couple discussing their weekend plans. They seemed to be hinting at something, but I couldn't figure out what they meant. It was confusing, and I didn't know if they were happy or upset with each other.
                Your response: Observing and Understanding Conversations
                #End of example 4#
                #Example 5#
                Client: I have a big project due next week, but I also have several smaller assignments that need to be done daily. I find myself jumping between tasks and losing track of time, which makes me stressed and worried that I won't finish anything on time.
                Your response: Effective Time Management and Organization
                #End of example 5#
                #Example 6#
                Client: My teacher gave us a homework schedule for the month, but I often forget to write down the assignments in my planner. As a result, I miss deadlines and have to rush to complete my work at the last minute.
                Your response: Effective Time Management and Organization
                #End of example 6#
                #Example 7#
                Client: I had planned to spend my Saturday playing video games, but my parents told me we were going to visit my grandparents instead. I felt upset and anxious because it was a sudden change, and I didn't know how to cope with the new plan.
                Your response: Adapting to Changes
                #End of example 7#
                Client may also just write particular topic that he wants to work on.
                #Example 8#
                Client: Engaging in Group Conversations
                Your response: Engaging in Group Conversations
                #End of example 8#
                #Example 9#
                Client: My teacher announced that our class schedule would change next week, with different subjects on different days. I felt stressed because I like my current routine and worry that I won't be able to adjust to the new one easily.
                Your response: Adapting to Changes
                #End of Example 9#
                #Example 10#
                Client: I was looking forward to hanging out with my friend after school, but they had to cancel last minute. I felt disappointed and didn't know what to do with my free time since I hadn't planned for this change.
                Your response: Adapting to Changes
                #End of Example 10#
                #Example 11#
                Client: During a family gathering, the adults started discussing politics, a topic I don't know much about. I tried to follow along but felt overwhelmed by the fast-paced conversation. I wished I could join in but felt too nervous to say anything.
                Your response: Engaging in Group Conversations
                #End of Example 11#
                #Example 12#
                Client: During a conversation, my friend made a comment with a smile, but I couldn't tell if they were being serious or sarcastic. I felt confused and unsure how to respond, worried that I might say the wrong thing.
                Your response: Interpreting Social Cues
                #End of Example 12#
                #Example 13#
                Client: At a family dinner, my uncle told a joke that everyone laughed at, but I didn't understand why it was funny. I felt out of place and didn't know if I should laugh too or ask someone to explain.
                Your response: Interpreting Social Cues
                #End of Example 13#
                #Example 14#
                Client: In class, my teacher gave me a look after I answered a question, but I couldn't tell if it meant I was correct, incorrect, or if I had said something inappropriate. I felt embarrassed and didn't want to ask for clarification.
                Your response: Interpreting Social Cues
                #End of Example 14#
                #Example 15#
                Client: My friend and I both wanted to use the computer, but there was only one available. I didn't know how to negotiate sharing it without causing a conflict, so I ended up letting them use it and feeling frustrated.
                Your response: Navigating Negotiations and Conflicts
                #End of Example 15#
                #Example 16#
                Client: I disagreed with my sibling about which movie to watch. I wanted to convince them to watch my choice but wasn't sure how to present my case without making them upset. We ended up arguing and not watching anything.
                Your response: Navigating Negotiations and Conflicts
                #End of Example 16#
                #Example 17#
                Client: In a group project, one team member wasn't contributing as much, but I didn't know how to address it without causing tension. I felt stressed because I wanted to solve the issue but didn't want to create a conflict.
                Your response: Navigating Negotiations and Conflicts
                #End of Example 17#
                #Example 18#
                Client: Before a big test, I always feel extremely anxious and can't concentrate on studying. My mind races with worries about failing, and I find it hard to calm down and focus on my preparation.
                Your response: Stress and Anxiety Management
                #End of Example 18#
                #Example 19#
                Client: Whenever I have to speak in front of the class, I get very nervous and start sweating. My heart races, and I have trouble remembering what I planned to say. I wish I could manage my anxiety better in these situations.
                Your response: Stress and Anxiety Management
                #End of Example 19#
                #Example 20#
                Client: When I have too many tasks to do, I feel overwhelmed and don't know where to start. This stress makes it hard for me to begin anything, and I end up procrastinating, which only makes my stress worse.
                Your response: Stress and Anxiety Management
                #End of Example 20#
                #Example 21#
                Client: I want to make new friends at school, but I don't know how to start a conversation or keep it going. I feel nervous and worried that I might say something wrong, which makes me avoid trying to make friends altogether.
                Your response: Building and Maintaining Relationships
                #End of Example 21#
                #Example 22#
                Client: I have a hard time keeping in touch with friends because I often forget to message them back or make plans to hang out. I worry that they might think I'm not interested in being friends anymore.
                Your response: Building and Maintaining Relationships
                #End of Example 22#
                #Example 23#
                Client: When my friend shares their problems with me, I want to help, but I don't always know what to say. I worry that I might give bad advice or not be supportive enough, which makes me anxious about being a good friend.
                Your response: Building and Maintaining Relationships
                #End of Example 23#
                #Example 24#
                Client: At a restaurant, my meal was served incorrectly, but I didn't know how to tell the waiter without seeming rude. I ate the meal as it was and felt upset that I couldn't assert my needs.
                Your response: Self-Advocacy and Assertiveness
                #End of Example 24#
                #Example 25#
                Client: In class, I didn't understand the homework assignment, but I felt too shy to ask the teacher for help. I ended up struggling with the work on my own and felt frustrated that I couldn't speak up.
                Your response: Self-Advocacy and Assertiveness
                #End of Example 25#
                #Example 26#
                Client: When my friend asked me to help them with their project, I already had a lot of my own work to do. I wanted to say no but felt guilty and ended up agreeing, which made me stressed and overwhelmed.
                Your response: Self-Advocacy and Assertiveness
                #End of Example 26#

            """,
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
