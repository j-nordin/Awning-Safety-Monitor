import os
import requests


def send(title: str, message: str):
    r = requests.post("https://api.pushover.net/1/messages.json", data={
        "token": os.environ["PUSHOVER_TOKEN"],
        "user": os.environ["PUSHOVER_USER_KEY"],
        "title": title,
        "message": message
    })

    if r.json()['status'] != 1:
        raise Exception(f"Could not send notification, response: {r.json()}")
    return r.json()
