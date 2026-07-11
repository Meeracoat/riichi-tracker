import requests


API_URL = "https://rc.honk.li/api/log"


def get_replay(log_id):

    response = requests.post(
        API_URL,
        json={
            "log_id": log_id
        },
        timeout=10
    )

    response.raise_for_status()

    return response.json()
