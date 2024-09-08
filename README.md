### Slack bot that wishes everyone on the channel on their birthday with a haiku

1. Clone the repository

    ```git clone https://github.com/sahil-s-246.com/Birthday-Bot.git```

2. Install Requirements

    ```pip install -r requirements.txt```

3. Run Main

    ```python3 main.py```

- Uses Googlesheets to keep track of the birthdays, dependency includes gspread
- Create a dot env file and enter the follwing value in the sample.env : 
- For google sheets, get the credentials from the sheets api on Google Cloud Console
- Slack tokens and secrets are on your api.slack.com dashboard
- s_url is the google sheet id
- c_id is channel id