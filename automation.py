import requests


def if_auto(agent, device_ip, if_name, port=None):
    if port:
        url = f"http://{agent}:{port}/cmd"
    else:
        url = f"http://{agent}/cmd"

    payload = {"need_fix": [device_ip, if_name]}
    response = requests.post(url, json=payload)
    if response.ok:
        return "OK"
    else:
        return response.text