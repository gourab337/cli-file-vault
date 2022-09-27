import requests
import json
import urllib3

urllib3.disable_warnings()


def Login(ip: str, port: int, username: str, password: str):
    url = "https://"+ip+":"+str(port)+"/rest/v1/login/sessions"
    payload = json.dumps({
        "username": username,
        "password": password,
        "setCookie": True
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload, verify=False)
    data = json.loads(response.text)
    if "errorString" in data:
        return data["errorString"]
    else:
        return data["token"]


def Alarm_trigger(ip: str, port: int, token: str, source: str, caption: str, description: str):
    url = "https://"+ip+":"+str(port)+"/api/createEvent"

    payload = json.dumps({
        "source": source,
        "caption": caption,
        "description": description
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+token,
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload, verify=False)
    data = json.loads(response.text)
    if "errorId" in data:
        if data["errorId"] == "ok":
            return "ok"
        else:
            return data["errorString"]


def save_rules(token: str, caption: str, resource: str, actionType: str, actionResourceIds: list):
    actionParams = {
        "additionalResources": [
            "{00000000-0000-0000-0000-100000000000}",
            "{00000000-0000-0000-0000-100000000001}"
        ],
        "allUsers": False,
        "authType": "authBasicAndDigest",
        "durationMs": 5000,
        "forced": True,
        "fps": 10,
        "needConfirmation": False,
        "playToClient": True,
        "recordAfter": 0,
        "recordBeforeMs": 0,
        "streamQuality": "highest",
        "useSource": False
    }
    eventCondition = {
        "caption": caption,
        "eventTimestampUsec": "0",
        "eventType": "undefinedEvent",
        "metadata": {
            "allUsers": False,
            "level": ""
        },
        "omitDbLogging": False,
        "reasonCode": "none",
        "resourceName": resource
    }
    payload = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "eventType": "userDefinedEvent",
        "eventCondition": json.dumps(eventCondition),
        "eventState": "active",
        "actionType": actionType,
        "actionResourceIds": actionResourceIds,
        "actionParams": json.dumps(actionParams),
        "aggregationPeriod": 0,
        "disabled": False
    }
    payload = json.dumps(payload)
    url = "https://192.168.124.27:7001/ec2/saveEventRule"

    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+token
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload, verify=False)
    res = json.loads(response.text)
    if (res["id"] != None):
        return res["id"]
