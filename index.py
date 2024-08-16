from flask import Flask, request, jsonify
from slack_bolt.adapter.flask import SlackRequestHandler
from message_counter import slack_app
from waitress import serve

# Listens to incoming messages that contain "hello"

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
    # app.run(port=5000, host="localhost") # for dev mode
    serve(app, host="0.0.0.0", port=5000)
