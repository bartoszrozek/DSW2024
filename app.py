from shiny import App, reactive, render, ui
from src.conversation import Conversation

app_ui = ui.page_fluid(
    ui.include_css("styles.css"),
    ui.panel_title("GPTherapy"),
    ui.output_ui("conversation_ui"),
    ui.row(
        ui.column(8, ui.input_text("new_message", "", width="100%")),
        ui.column(4, ui.input_action_button("new_message_button", "Send")),
        class_="input-message-bar",
    ),
)


def server(input, output, session):
    conversation = Conversation()

    @reactive.effect
    @reactive.event(input.new_message_button)
    def add_new_message() -> None:
        conversation.new_message(input.new_message(), "user")
        new_message = conversation.last_message()
        ui.insert_ui(
            new_message.generate_ui(),
            selector="#conversation_ui",
            where="afterEnd",
        )


app = App(app_ui, server)
