# This file runs on the Raspberry Pi.
# It requires to have  'capture' and 'output' directories created inside the directory this is placed in.
# Configuration should be in a .env in the same directory as this file.

import datetime
import logging
import os
import pathlib
import subprocess
import time

import dotenv
import requests
from libcamera import controls
from picamera2 import Picamera2

TWENTY_SECONDS = 20
SIXTY_SECONDS = 60
SLEEP_INTERVAL = 20
FULL_HD = (1920, 1080)
HD = (1280, 720)


dotenv.load_dotenv()

CALL_NAME = os.getenv("CALL_NAME")
VENDOR = os.getenv("VENDOR")
DEVICE_TYPE = os.getenv("DEVICE_TYPE")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

INTERVAL = 5


def setup() -> Picamera2:
    picam2 = Picamera2()
    picam2.controls.set_controls({"AfMode": controls.AfModeEnum.Continuous})
    # for i in range(100):
    #     print(i)
    #     logging.log(logging.INFO, f"Attmpting to autofocus on try #{i}.")
    #     if picam2.autofocus_cycle():
    #         print(6)
    #         break
    # config = picam2.create_preview_configuration(main={"size": HD})

    # picam2.configure(config) # type: ignore
    logging.log(logging.INFO, f"Picamera is configured.")
    picam2.start()
    time.sleep(2)
    logging.log(logging.INFO, f"Picamera is started.")
    return picam2


def loop(picamera: Picamera2, next_valid_time=None) -> datetime.datetime:
    # UNIX timestamp
    current_time = datetime.datetime.now(datetime.timezone.utc)
    current_unix_timestamp = int(current_time.timestamp())

    if not next_valid_time:
        next_valid_time = compute_next_valid_time(current_time, INTERVAL)
        return next_valid_time

    if next_valid_time and current_time < next_valid_time:
        time.sleep(SLEEP_INTERVAL)
        return next_valid_time

    # check the current time
    if (current_time.minute % INTERVAL) == 0:
        logging.log(logging.INFO, "Capturing photo.")
        capture_photo(picamera, current_unix_timestamp)
        next_valid_time = compute_next_valid_time(current_time, INTERVAL)

    if current_time.minute == 0 or current_time.minute == 30:
        logging.log(logging.INFO, "Taking time-lapse.")
        time_lapse = write_time_lapse_mp4(current_unix_timestamp)
        logging.log(logging.INFO, "Sending time-lapse.")
        response = send_request_to_server(time_lapse, current_unix_timestamp)
        logging.log(
            logging.INFO,
            f"The response status code was: {response.status_code}, with reason: {response.reason}.",
        )

    return next_valid_time


def compute_next_valid_time(current_time: datetime.datetime, interval_of_minutes: int):
    minutes_to_next_valid_time = interval_of_minutes - (
        current_time.minute % interval_of_minutes
    )
    return current_time + datetime.timedelta(minutes=minutes_to_next_valid_time)


def capture_photo(picam2: Picamera2, current_time: int):
    filename = f"capture_{CALL_NAME}_{current_time}.jpg"
    capture_full_path = pathlib.Path(os.getcwd()) / "capture" / filename
    picam2.capture_file(capture_full_path)


def write_time_lapse_mp4(current_time: int) -> pathlib.Path:
    framerate: str = str(12)
    output_file_path = (
        pathlib.Path(os.getcwd()) / "output" / f"time_lapse_{current_time}.mp4"
    )
    capture_file_path = (
        pathlib.Path(os.getcwd()) / "capture" / f"capture_{CALL_NAME}_*.jpg"
    )
    shell_command = [
        "ffmpeg",
        "-framerate",
        framerate,
        "-pattern_type",
        "glob",
        "-i",
        capture_file_path,
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-vf",
        "scale=1280:720",
        output_file_path,
    ]
    subprocess.run(shell_command)
    return output_file_path


def send_request_to_server(filepath_to_send_to_server: pathlib.Path, current_time: int):
    with open(filepath_to_send_to_server, "rb") as file:
        files = {"file": (filepath_to_send_to_server.name, file.read())}

    url = "https://projectevergreen.live/relay-upload"
    data = {
        "Call-Name": CALL_NAME,
        "Relay-Device-Auth-Token": AUTH_TOKEN,
        "Vendor": VENDOR,
        "Device-Type": DEVICE_TYPE,
        "UNIX-Timestamp": current_time,
    }
    response = requests.post(url=url, data=data, files=files)
    return response


def main():
    if not CALL_NAME or not VENDOR or not DEVICE_TYPE or not AUTH_TOKEN:
        print("Environment variable(s) not set. ")
        exit(1)

    logging.basicConfig(
        filename="time_lapse.log",
        level=logging.INFO,
        format="%(asctime)s : %(levelname)s : %(message)s",
    )
    current_time = datetime.datetime.now(datetime.timezone.utc)
    logging.log(logging.INFO, f"Starting main.")
    while True:
        try:
            logging.log(logging.INFO, "Starting setup.")
            picamera = setup()
            next_valid_time = None
            while True:
                logging.log(logging.INFO, "Starting loop.")
                next_valid_time = loop(picamera, next_valid_time)
        except Exception:
            continue
        finally:
            return


if __name__ == "__main__":
    main()
