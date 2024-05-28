import streamlit as st
from openai import OpenAI
import conversations.starting_message as msg
import src.assistants as assistants
import os
import datetime

client = OpenAI()

st.set_page_config(layout="wide")

st.title("Chat-Bot Therapy")

language_option = st.selectbox("Language", ("English", "Polski"))

extractor = assistants.Extractor(language_option)
screenwriter = assistants.Screenwriter(language_option)
analist = assistants.Analist(language_option)
concluser = assistants.Concluser(language_option)
compariser = assistants.Compariser(language_option)
organizer = assistants.Organizer(language_option)
conversationalist = assistants.Conversationalist(language_option)

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

if "start_timestamp" not in st.session_state:
    st.session_state["start_timestamp"] = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


with st.chat_message("assistant"):
    st.markdown(msg.welcome_message[language_option])

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Logging: Write a log of the interaction
os.makedirs("logs", exist_ok=True)
log_filename = f'logs/{st.session_state["start_timestamp"]}.log'

# React to user input
if prompt := st.chat_input("Insert to chat"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


    # Logging prompt
    with open(log_filename, 'a') as f:
        f.write(f"<< User >>: {prompt}\n")

    organization = organizer.ask_assistant(
        prompt,
        ", ".join(
            [
                f"{msg.message_intro[language_option]} {idx}: {message}"
                for idx, message in enumerate(
                    st.session_state["messages"]
                )
            ]
        )
    )
    
    # Logging organisation
    print(f"------{organization}------")
    with open(log_filename, 'a') as f:
        f.write(f"------{organization}------\n")

    if organization == "Extractor":
        problem = extractor.ask_assistant(prompt)

        # Logging problem
        print(msg.identified_problem[language_option] + problem)
        with open(log_filename, 'a') as f:
            f.write(msg.identified_problem[language_option] + problem + "\n ")

        response, st.session_state.name = screenwriter.ask_assistant(problem)
        st.session_state.story = response
        
    elif organization == "Compariser":
        if st.session_state.name == "" or st.session_state.story == "":
            response = (
                msg.missed_some_steps[language_option]
                + msg.starting_message[language_option]
            )
        else:
            st.session_state.therapist_description = concluser.ask_assistant(
                st.session_state.story, st.session_state.name
            )


            # Logging Concluser output
            with open(log_filename, 'a') as f:
                f.write(f"Concluser: {st.session_state.therapist_description}\n")

            if st.session_state["descriptions"] != []:
                response = compariser.ask_assistant(
                    st.session_state.therapist_description,
                    prompt,
                    ", ".join(
                        [
                            f"{msg.description_intro[language_option]} {idx}: {description}"
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
                    f"{msg.description_intro[language_option]} {idx}: {message}"
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
        response = not_understand[language_option]

    with st.chat_message("assistant"):
        st.markdown(response, unsafe_allow_html=True)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Logging response
    with open(log_filename, 'a') as f:
        f.write(f"<< Assistant >>: {response}\n")
