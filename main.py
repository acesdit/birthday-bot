import os
from slack_bolt import App
from get_birthdays import get_values
import google.generativeai as genai

# Initializes your app with your bot token and socket mode handler
slack_app = App(
    token=os.getenv("SLACK_BOT_TOK"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")  # not required for socket mode
)
genai.configure(api_key=os.getenv("gemini"))

channel_id = os.getenv("c_id")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


def get_id(name):
    users_list = slack_app.client.users_list()["members"]

    user_dict = {user["id"]: user["profile"]["real_name"] for user in users_list}
    for user in user_dict:
        if user_dict[user] == name:
            return user  # returns id


def get_prompt() -> str:
    names = get_values()
    first_names = [name.split(" ")[0] for name in names]

    if len(names) > 0:  # Ensure there are birthdays to process
        prompt = f"""
            
            haiku with the following name(s):
            {first_names}

            the main message of haiku is a birthday message

            Proper 5-7-5 haiku format
            eg:
            prompt: haiku with the name sahil in it
            the main message of haiku is a birthday message:

            respond in the format:
            
            Sahil, guide on shore,
            Happy birthday, leader bright,
            May your path be clear.

            One haiku for each name
            Followed by the definition of haiku in a line
                    
         """
        try:

            response = model.generate_content(prompt).text
            return response
        except Exception as e:
            print(f"Error generating content: {e}")
            return "no"  # Return "no" if there's an error with API call
    return "no"


# Generate the prompt and post to Slack if there are birthdays
response_text = get_prompt()

if response_text != "no":
    try:
        response = slack_app.client.chat_postMessage(
            channel=channel_id,  # Channel ID or user ID to send a message to
            text=response_text,  # Text of the message

        )
        print(f"Message sent to {channel_id}: {response['message']['text']}")
    except Exception as e:
        print(f"Error sending message: {e}")
else:
    print("No birthdays today. No message sent.")
