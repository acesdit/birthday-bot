import os
from slack_bolt import App
from add_to_google_sheets import append_to_sheet, get_values
import logging

logging.basicConfig(level=logging.DEBUG)
# Initializes your app with your bot token and socket mode handler
slack_app = App(
    token=os.getenv("SLACK_BOT_TOK"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET") # not required for socket mode
)


# Listens to incoming messages that contain "hello"
@slack_app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )


@slack_app.message(r'^(sa|sb|sc|sd|ta|tb|tc|td)$')
def update_status(message, say):
    # say() sends a message to the channel where the event was triggered
    t = list(message["text"].upper())
    t.insert(1,"E-")  # ta to TE-A
    div = "".join(t)
    status, values = append_to_sheet(div)
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Message shared:*\n```{values}```\n\n*Status:*\n{status}"
                }
            }
        ],
        text=f"Message shared: {values}\nStatus: {status}"  # Fallback text for notifications
    )


@slack_app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


@slack_app.command("/check")
def get_status(ack, say, command):
    # Acknowledge command request
    ack()
    values, status = get_values()
    say(f"Status:\n\n{values}\n\n{status}")


@slack_app.event("app_mention")
def get_status(ack, say, command):
    # Acknowledge command request
    ack()
    values, status = get_values()
    say(f"Status:\n\n{values}\n\n{status}")

# @slack_app.event("message")
# def handle_message_events(body, logger):
#     logger.info(body)
#
#
# @slack_app.middleware  # or app.use(log_request)
# def log_request(logger, body, next):
#     logger.debug(body)
#     return next()

