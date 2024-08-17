from flask import Flask, request, jsonify
from slack_bolt.adapter.flask import SlackRequestHandler
from message_counter import slack_app
from waitress import serve
app = Flask(__name__)
handler = SlackRequestHandler(slack_app)


@app.route("/", methods=["GET", "POST"])
def main():
    return "Hello World!"


@app.route("/slack/events", methods=["POST"])
def slack_events():
    # if request.content_type == "application/json":
    #     return {"challenge": request.json["challenge"]}
    return handler.handle(request)


if __name__ == "__main__":
    # SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()
    # app.run(port=5000, host="localhost") # for dev mode
    serve(app, host="0.0.0.0", port=5000)
