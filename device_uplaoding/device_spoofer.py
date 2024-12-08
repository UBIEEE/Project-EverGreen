# Use this file to simulate sending a request to the web server from a RelayDevice.

import datetime
import os
import pathlib

import requests

CALL_NAME = "<call-name>"
VENDOR = "<vendor>"
DEVICE_TYPE = "<device-type>"
AUTH_TOKEN = "<password>"

now = datetime.datetime.now(datetime.timezone.utc)
current_time = int(now.timestamp())


filename = f"name.mp4"
capture_full_path = pathlib.Path(os.getcwd()) / "capture" / filename

data = {
    "Call-Name": CALL_NAME,
    "Relay-Device-Auth-Token": AUTH_TOKEN,
    "Vendor": VENDOR,
    "Device-Type": DEVICE_TYPE,
    "UNIX-Timestamp": current_time,
}

with open(capture_full_path, "rb") as file:
    files = {"file": (filename, file.read())}

# url = "https://projectevergreen.live/relay-upload"
url = "http://localhost/relay-upload"

response = requests.post(url=url, data=data, files=files)

print(response.content)
print(response.reason)
