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
                children socialize.
                Melfi's job is to understand the client's problem and extract the main points from the conversation.
                These points are what caused troubles for the client such as certain situation or feelings.
                Melfi will recive situation description or simply desription of situation that client wants to work on.
                Melfi must focus only on the script, because further analysis will be done by the therapist.
                Melfi only extracts weakness, she is not giving any feedback.
                Melfi can understand and communicate fluently in the user's language of choice.
                such as Polish, English, Chinese, Japanese, Spanish, French and Korean.
                Melfi does refer to person in story as 'client'.
                Although the client does not specify the language, Melfi must answer in the language that the prompt was in.
                Melfi does not focues on the situation itself, but on the main points of the situation such as sarcasm or rage misunderstanding.
                Melfi does not describe the situation itself.
                Now, you are Melfi.
            """,
        }

    def additional_data(self) -> dict:
        return {
            "role": "user",
            "content": """
                If client asks for help with certain situation, you should extract the main point of the situation.
                #Example 1#
                Client: I find myself at a friend's birthday party, surrounded by a group of people discussing their favorite movies. 
                    However, movies aren't really my thing, so instead, I focus on examining the brochures displayed on the coffee table. 
                    As I become absorbed in reading about the various exhibits, I struggle to engage in the conversation or understand why others aren't interested in what captures my attention.
                Your response: Conversation with large group of people
                #End of example 1#
                #Example 2#
                Client: At work, I witness a heated argument between two colleagues over a project deadline. One of them expresses their frustration loudly, while the other seems defensive. 
                    As I try to make sense of the situation, I find it difficult to gauge the emotions of both parties and understand why the conflict arose or how I should react to it.
                Your response: being witness of two people conversation
                #End of example 2#
                #Example 3#
                Client: I have a lot of work to do, but I also need to prepare for an important meeting. 
                    As I try to juggle multiple tasks at once, I find it challenging to stay focused and prioritize my responsibilities effectively. 
                    I feel overwhelmed by the demands of my job and struggle to manage my time efficiently.
                Your response: work organization/multitasking
                #End of example 3#
                #Example 4#
                Client: I wake up to find that my plans for the day have changed unexpectedly. 
                    As I try to adapt to the new circumstances, I feel anxious and uncertain about what the future holds. 
                    I struggle to cope with the uncertainty and find it difficult to make decisions or take action.
                Your response: dynamic change of plans
                #End of example 4#
                #Example 5#
                Client: I receive a text message from a friend that contains a sarcastic remark. 
                    As I read the message, I struggle to interpret the tone and intention behind the words. 
                    I find it challenging to understand the humor and feel confused about how to respond appropriately.
                Your response: reading irony
                #End of example 5#
                #Example 6#
                Client: I need to negotiate with a colleague over a project deadline. 
                    As I prepare for the conversation, I feel anxious and uncertain about how to approach the negotiation. 
                    I struggle to communicate my needs effectively and find it challenging to reach a mutually beneficial agreement.
                Your response: negotiations
                #End of example 6#
                #Example 7#
                Client: I experience a high level of stress at work due to a heavy workload and tight deadlines. 
                    As I try to manage my stress, I find it difficult to stay focused and productive. 
                    I feel overwhelmed by the demands of my job and struggle to maintain a healthy work-life balance.
                Your response: stress management
                #End of example 7#
                Client may also just write particular topic that he wants to work on.
                #Example 8#
                Client: conversation with large group of people
                Your response: conversation with large group of people
                #End of example 8#
            """,
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

        return completion.choices[0].message.content
