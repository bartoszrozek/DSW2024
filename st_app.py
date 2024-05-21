import streamlit as st
from openai import OpenAI
import conversations.starting_message as msg
import src.assistants as assistants

client = OpenAI()
extractor = assistants.Extractor()
screenwriter = assistants.Screenwriter()
analist = assistants.Analist()
concluser = assistants.Concluser()
compariser = assistants.Compariser()
organizer = assistants.Organizer()
conversationalist = assistants.Conversationalist()

st.set_page_config(layout="wide")

st.title("Chat-Bot Therapy")

language_option = st.selectbox("Language", ("English", "Polski"))

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "description" not in st.session_state:
    st.session_state["descriptions"] = []

for variable in [
    "user_description",
    "therapist_description",
    "name",
    "story",
]:
    if variable not in st.session_state:
        st.session_state[variable] = ""


with st.chat_message("assistant"):
    st.markdown(msg.welcome_message[language_option])

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Insert to chat"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    organization = organizer.ask_assistant(prompt, 
                                           ", ".join(
                                                    [
                                                        f"Message {idx}: {message}"
                                                        for idx, message in enumerate(
                                                            st.session_state["messages"]
                                                        )
                                                    ]
                                                ))
    print(f"------{organization}------")
    if organization == "Extractor":
        problem = extractor.ask_assistant(prompt)
        print(f"Identified problem: {problem}")
        response, st.session_state.name = screenwriter.ask_assistant(problem)
        st.session_state.story = response
        
    elif organization == "Compariser":
        if st.session_state.name == "" or st.session_state.story == "":
            response = (
                "I think we missed some steps. Please start from the beggining.\n"
                + msg.starting_message[language_option]
            )
        else:
            st.session_state.therapist_description = concluser.ask_assistant(
                st.session_state.story, st.session_state.name
            )
            if st.session_state["descriptions"] != []:
                response = compariser.ask_assistant(
                    st.session_state.therapist_description,
                    prompt,
                    ", ".join(
                        [
                            f"Description {idx}: {description}"
                            for idx, description in enumerate(
                                st.session_state["descriptions"]
                            )
                        ]
                    ),
                )
            else:
                response = compariser.ask_assistant(
                    st.session_state.therapist_description, prompt
                )
            st.session_state["descriptions"].append(prompt)

    elif organization == "Conversationalist":
        response = conversationalist.ask_assistant(
                    prompt,
                    ", ".join(
                        [
                            f"Message {idx}: {message}"
                            for idx, message in enumerate(
                                st.session_state["messages"]
                            )
                        ]
                    ),
                )

    elif organization == "New conversation":
        response = msg.starting_message[language_option]
        for variable in [
            "user_description",
            "therapist_description",
            "name",
            "story",
        ]:
            if variable not in st.session_state:
                st.session_state[variable] = ""

    else:
        print(f"Value of organization: {organization}")
        response = "I do not know understand. Please provide more information."

    with st.chat_message("assistant"):
        st.markdown(response, unsafe_allow_html=True)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
