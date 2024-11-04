# Project Evergreen

Project Evergreen is a group project for the class [CSE312: Web Applications](https://cse312.com/) at the University at Buffalo in the Fall 2024 semester. This project is intended to become the web application for the UB IEEE student chapter automated greenhouse project. You can find out more information on [our Discord](https://discord.com/invite/QMHjt65z7a). 


## Managing the Local Environment

The development environment is being managed using [Poetry](https://python-poetry.org/). Please make sure that you have Poetry installed:
```shell
pip install poetry
```

The virtual environment can be created locally by using the `poetry install` command from the `evergreen` directory. The environment can then be activated using the `poetry shell` command. This venv can then be deactivated by using the `exit` command.

New package dependencies for the project can be added using the `poetry add <package-name-from-pip>` command.


## Setting up the Docker Environment

In the root directory of the project, type `docker compose up --build --force-recreate` to spin up the containers. The poetry environment does not need to be activated for this. 

The database migrations should be automatically applied by Docker when it spins up the containers. If you are receiving errors during this step, it is best to delete any old containers and volumes you have lying around to ensure that Docker creates the setup form a clean state. 

> [!TIP]
> We have noticed that the containers do not attach properly if a user is running docker through the `mnt/c/` directory when using [WSL](https://learn.microsoft.com/en-us/windows/wsl/). Please have the project placed directly in your host filesystem and spin up the containers directly from your host OS. 

You can use the command `docker compose exec django python manage.py createsuperuser` to make your admin user from a separate terminal. You can then go to the `/admin` panel and login with those credentials that you used to create the super user. 
