import requests

SERVER_URL = "http://127.0.0.1:8000"

def send_report(data):
    return requests.post(
        f"{SERVER_URL}/report",
        json=data
    )