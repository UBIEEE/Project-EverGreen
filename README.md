# Project Evergreen

Project Evergreen is a group project for the class [CSE312: Web Applications](https://cse312.com/) at the University at Buffalo in the Fall 2024 semester. This project is intended to become the web application for the UB IEEE student chapter automated greenhouse project. You can find out more information on [our Discord](https://discord.com/invite/QMHjt65z7a). 

The project can be found at: https://projectevergreen.live/

## Managing the Local Environment

### Env
On a fresh clone of the repository, make sure that when testing locally to rename the .env.example to .env before running docker-compose. This is for security of the repository.

### Poetry
The development environment is being managed using [Poetry](https://python-poetry.org/). Please make sure that you have Poetry installed:
```shell
pip install poetry
```

The virtual environment can be created locally by using the `poetry install` command from the `evergreen` directory. The environment can then be activated using the `poetry shell` command. This venv can then be deactivated by using the `exit` command.

New package dependencies for the project can be added using the `poetry add <package-name-from-pip>` command.

### Nginx for Localhost
To set up nginx configuration, a self signed certificate is needed. To set this up, in the terminal run:
```shell
openssl req -x509 -newkey rsa:4096 -keyout private.key -out cert.pem -days 365 -sha256 -nodes
```

Only the "Country Name" field is necessary, in which you should should type "us" then press enter. All other fields may be ignored by typing "." and pressing enter.

Make sure the files are placed in the nginx file directory.

## Setting up the Docker Environment

In the root directory of the project, type `docker compose up --build --force-recreate` to spin up the containers. The poetry environment does not need to be activated for this. 

The database migrations should be automatically applied by Docker when it spins up the containers. If you are receiving errors during this step, it is best to delete any old containers and volumes you have lying around to ensure that Docker creates the setup form a clean state. 

> [!TIP]
> We have noticed that the containers do not attach properly if a user is running docker through the `mnt/c/` directory when using [WSL](https://learn.microsoft.com/en-us/windows/wsl/). Please have the project placed directly in your host filesystem and spin up the containers directly from your host OS. 

You can use the command `docker compose exec django python manage.py createsuperuser` to make your admin user from a separate terminal. You can then go to the `/admin` panel and login with those credentials that you used to create the super user. 

## Redirects

Please note that requests to port 8080 are redirected to port 80 or 443 as static files are hosted through nginx. Port 443 is used in instances where certs are present. Port 80 is used in instances where they are not present. Requests to port 80 will be upgraded to HTTPS (443) if that is in use.


## Creativity and Documentation: Sending time-lapse videos from IoT device / admin commands to register IoT device.

### Feature Explanation

Since this webserver is meant to control IoT devices and receive data form IoT devices, we implemented a feature where a user can create an IoT device that uploads data to the server securely.

At the current time, we have it set up so that a Raspberry Pi can upload time-lapses of plant growth. The code for the webserver running on the Pi can be found at `device-uploading/time_lapse.py`. However, since we do not expect a TA to set up or have a Raspberry Pi to test this (and it would be difficult to do anyway when testing of localhost) we have included a file that can be used to simulate/spoof what the raspberry pi is doing from your own computer. This file can be found at `device_uploading/device_spoofer.py`.

Additionally, to help an admin user manage these devices, we have created admin commands inside of Django that allows the admin to register, de-activate, and activate a device. They are as follows:
- `register_relay_device`: Registers a new device into the database, sets it as active, and returns to the admin user the auth-token/password to upload for that device's authentication.
- `deactivate_relay_device`: Marks a device as de-activated and will reject any requests coming from this device even if it has a valid authentication token.
- `activate_relay_device`: Marks a device as activated and will allow and requests coming from this device when it has valid authentication credentials.

We believe both the features for the time-lapse uploads from the Pi _and_ the admin commands both count as separate valid features for the purposes of Part 3 Objective 3. Even if you do not count the Pi stuff since we cannot have you run the script on a Pi to our web server to test, the admin commands should still be sufficient to count as the additional feature.

### Testing Procedure

> [!TIP] 
> These testing procedures are long and delicate. Please read _all_ of the testing procedure before starting to avoid making errors.

1. Locate the file `device_spoofer.py` inside the `device_uploading` directory. Copy this to a totally new and separate location on your computer from the directory/repo for this project. For example, if you cloned this repo so that it is at `~Projects/Grading/Project-EverGreen/` then you could move this file to `~/Projects/Grading/Spoofing/`.

2. Inside of the directory in which you copied `device_spoofer.py`, also create a new directory that is named `capture`. For example, if you placed `device_spoofer.py` at `~/Projects/Grading/Spoofing/device_spoofer.py`, you should have a directory `~/Projects/Grading/Spoofing/capture/`.

3. Place at least three unique `.mp4` files that are less than 40MB in size with unique names inside of the `capture` directory you just created. These will be used for testing. It is important that they are all different files with different contents _and_ different filenames.

4. Spin up the containers to launch the app locally. You can do this using the command `docker compose up --build --force-recreate` from the directory you placed the project/repo.

5. Once the containers are finished, navigate to `localhost` using your browser and verify that the Project Evergreen site shows up. It is ok and expected for no video to be showing at this point where the time-lapse is supposed to be.

6. Open up a new terminal from the same path that you where at when you did docker compose. From this directory, verify that the django, postgres, and nginx containers for this app are running using the command `docker ps`. Now, open a bash shell inside of the django containers. How exactly you do this might change depending on how you installed docker on your system. We used the command `docker compose exec django bash`. You could also use the command `docker exec -it <container-id-of-django> bash`. If neither of these commands worked for you, you will have to google how to open up a bash shell inside of a docker container for the way that you installed docker.

7. Once you are inside the container, you will execute the command to register a new device. In the root directory of the django container, run the command `python manage.py register_relay_device <call-name> <vendor> <device-type>`. Make sure that the inputs you use contain only valid ASCII alphanumeric characters. For example, if I was registering a RPi whose name I wanted to be "PiCam", I would do `python manage.py register_relay_device "PiCam" "RaspberryPi" "4b"`. This command should output a password/auth-token that you will use to send requests. Copy this password _and_ the call-name that you named the device so that you have them for later. _You will use this terminal again later, keep it open._

8. Copy the information you used to register the device into the corresponding variables on lines 9-14 in `device_spoofer.py`. Also, change the value of the `filename` variable to be the filename of the first file you would like to test that you placed inside the `capture/` directory. For example, if you placed the file named `recording1.mp4` inside of `capture/`, you would have `filename = "recording1.mp4"`. Ensure that `CALL_NAME` is exactly the call name you used to register with and that `AUTH_TOKEN` is exactly the password outputted by the `register_relay_device` command.

```python
# contents of device_spoofer.py
 9 CALL_NAME = "<call-name>" # replace these
10 VENDOR = "<vendor>"
11 DEVICE_TYPE = "<device-type>"
12 AUTH_TOKEN = "<password>"
13 
14 filename = "<filename-with-extension>"
```

9. Run the python file `device_spoofer.py` with the command `python3 device_spoofer.py` inside the new directory you made for spoofing. Verify that the program gave a status code and response printed to the terminal indicating the the request/upload was successful. Go the your browser and refresh the page to confirm that the new video appears, you might have to wait ~30s for the app to process the new upload. (Some browsers may use a caching scheme which may prevent the new video from displaying right away on refresh, if this is the case simply open `localhost` from a new private window to verify the new video).

> [!IMPORTANT] 
> The `device_spoofer.py` script uses the `requests` package, if you do not already have it installed on your system you will have to install it with `pip3 install requests` or whatever other way you use to install 3rd party python packages on your system.

> [!CAUTION] 
> The testing procedures were written assuming that you are working from a fresh clone of the repo. If you created self-signed certs for the website the requests module is liable to blow up with SSL errors.

10. We will now de-activate the device you just registered. Return back to the terminal inside the django container. Now run the command `python manage.py deactivate_relay_device <call-name>` with the same call-name you used to register beforehand. Going of the previous example, this would be `python manage.py deactivate_relay_device "PiCam"`. Return back to the `device_spoofer.py` file and change the filename variable to one of the other `.mp4` files you placed inside the `capture/` directory. Run the `device_spoofer.py` script again and verify that it printed out a response code and message indicating that your upload request to the server was rejected. Verify that the video playing on the webpage did not change to the new video you attempted to send.

11. We will now re-activate the device you just registered. Return back to the terminal inside the django container. Now run the command `python manage.py activate_relay_device <call-name>` with the same call-name you used to register beforehand. Going of the previous example, this would be `python manage.py activate_relay_device "PiCam"`. Return back to the `device_spoofer.py` file and change the filename variable to one of the other `.mp4` files you placed inside the `capture/` directory that you have not used yet. Run the `device_spoofer.py` script again and verify that it printed out a response code and message indicating that your upload request to the server was accepted. Go the your browser and refresh the page to confirm that the new video appears, you might have to wait ~30s for the app to process the new upload. (Some browsers may use a caching scheme which may prevent the new video from displaying right away on refresh, if this is the case simply open `localhost` from a new private window to verify the new video).

12. Change the variables for `AUTH_TOKEN` and/or `CALL_NAME` to random strings in `device_spoofer.py`. Run `device_spoofer.py` and verify that the requests you send with these invalid credentials are rejected by the server.