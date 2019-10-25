import slack

from behind import settings

slack_client = slack.WebClient(token=settings.SLACK_BOT_ACCESS_TOKEN)


def send_slack(text, channel='#jarvis-help'):
    return slack_client.chat_postMessage(
        channel=channel,
        text=text,
        icon_emoji=':jarvis:'
    )
