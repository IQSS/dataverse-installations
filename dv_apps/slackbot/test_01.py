import json
from os import environ
from slackclient import SlackClient

SLACK_TEST_TOKEN = environ.get('SLACK_TEST_TOKEN')

slack_client = SlackClient(SLACK_TEST_TOKEN)

#print slack_client.api_call("api.test")
#print slack_client.api_call("auth.test")

def get_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call.get('ok'):
        return channels_call['channels']
    return None

def list_channels():

    channels = get_channels()
    if channels:
        print("Channels: ")
        for idx, c in enumerate(channels):
            print('\n(%s) %s %s' % (idx+1, c['name'], c['id']))
    else:
        print("Unable to authenticate.")

def get_channel_info(channel_id):
    channel_info = slack_client.api_call("channels.info", channel=channel_id)
    if channel_info:
        return channel_info['channel']
    return None

def json_dumps(info):
    print json.dumps(info, indent=4)


def get_test_attachement():
    return [dict(text='test test\ntwo lines',
                 image_url='https://dataverse.harvard.edu/logos/1/HarvardShield_RGB.png'
                 )]
    return """{
    "attachments": [
        {
            "fallback": "plain-text summary of the messsage.",
            "color": "#36a64f",
            "pretext": "Optional text that appears above the attachment block",
            "author_name": "DvBot",
            "author_link": "http://flickr.com/bobby/",
            "author_icon": "http://flickr.com/icons/bobby.jpg",
            "title": "Slack API Documentation",
            "title_link": "https://api.slack.com/",
            "text": "Optional text that appears within the attachment",
            "fields": [
                {
                    "title": "Priority",
                    "value": "High",
                    "short": false
                }
            ],
            "image_url": "http://my-website.com/path/to/image.jpg",
            "thumb_url": "http://example.com/path/to/thumb.png",
            "footer": "Slack API",
            "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
            "ts": 123456789
        }
    ]}"""

def send_message(channel_id, message, emoji=':robot_face:'):
    return slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        #attachments=get_test_attachement(),
        username='dvbot',
        icon_emoji=emoji
    )



if __name__ == '__main__':
    metrics_channel_id = 'C1V8PSV5Y'

    # list channels
    #list_channels()

    # get info on metrics channel
    #ci = get_channel_info('C1V8PSV5Y')
    #json_dumps(ci)

    # send test message
    sm = send_message(metrics_channel_id, 'send some highlights `print emoji`', ':traffic_light:')
    json_dumps(sm)

    #sm = send_message(metrics_channel_id, 'please go back to work (and drink some water)', ':computer')
    json_dumps(sm)


# Emojis
# http://www.webpagefx.com/tools/emoji-cheat-sheet/
