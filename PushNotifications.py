import os
import requests


def send_push_notification(title: str, message: str):
    r = requests.post("https://api.pushover.net/1/messages.json", data={
        "token": os.environ["PUSHOVER_TOKEN"],
        "user": os.environ["PUSHOVER_USER_KEY"],
        "title": title,
        "message": message
    })

