# Project Evergreen

Project Evergreen is a group project for the class [CSE312: Web Applications](https://cse312.com/) at the University at Buffalo in the Fall 2024 semester. This project is intended to become the web application for the UB IEEE student chapter automated greenhouse project. You can find out more information on [our Discord](https://discord.com/invite/QMHjt65z7a). 

The project can be found at: https://projectevergreen.live/



## Managing the Local Environment

## Env
On a fresh clone of the repository, make sure that when testing locally to rename the .env.example to .env before running docker compose

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

# Redirects

Please note that requests to port 8080 are redirected to port 80 or 443 as static files are hosted through nginx. Port 80 is used in instances where self signed certificates are not present, and 443 is used when they are.
