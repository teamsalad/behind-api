import slack
import os

slack_client = slack.WebClient(token=os.getenv('SLACK_BOT_ACCESS_TOKEN'))


def send_slack(text, icon_emoji=':jarvis:', channel='#jarvis-help'):
    return slack_client.chat_postMessage(
        channel=channel,
        text=text,
        icon_emoji=icon_emoji
    )
