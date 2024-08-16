from flask import Flask, request, jsonify
from waitress import serve

# Listens to incoming messages that contain "hello"

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def main():
    return "Hello World!"

# if __name__ == "__main__":
#     # SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()
#     # app.run(port=5000, host="localhost") # for dev mode
#     serve(app, host="0.0.0.0", port=5000)
