import requests


def if_auto(agent, port, device_ip, if_name):
    url = f"http://{agent}:{port}/cmd"
    payload = {"need_fix": [device_ip, if_name]}
    response = requests.post(url, json=payload)
