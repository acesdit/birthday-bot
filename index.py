from flask import Flask, request, jsonify
from slack_bolt.adapter.flask import SlackRequestHandler
# from message_counter import slack_app
from waitress import serve
from slack_bolt import App
import os

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


app = Flask(__name__)

req_handler = SlackRequestHandler(slack_app)


@app.route("/", methods=["GET", "POST"])
def main():
    return "Hello World!"


@app.route("/slack/events", methods=["POST"])
def slack_events():
    # if request.content_type == "application/json":
    #     return {"challenge": request.json["challenge"]}
    # slack sends a challenge token to this endpoint, and only then does it consider it as a legit request url
    return req_handler.handle(request)


if __name__ == "__main__":
    # SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()
    app.run(port=5000, host="localhost") # for dev mode
    # serve(app, host="0.0.0.0", port=5000)
