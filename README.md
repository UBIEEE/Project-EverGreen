# Project Evergreen

Project Evergreen is a group project for the class CSE312: Web Applications at the University at Buffalo in the Fall 2024 semester. This project is intended to become the web application for the UB IEEE student chapter automated greenhouse chapter. 

## Managing the Local Environment

The development environment is being managed using [Poetry](https://python-poetry.org/). Please make sure that you have Poetry installed:
```shell
pip install poetry
```

The virtual environment can be created locally by using the `poetry install` command from the `evergreen` directory. The environment can then be activated using the `poetry shell` command. This venv can then be deactivated by using the `exit` command. 

New package dependencies for the project can be added using the `poetry add <package-name-from-pip>` command. 


## Setting up the Docker Environment

Before starting up the container, make sure to run the command `python manage.py makemigrations` if you have made any changes to the database models. 

In the root directory of the project, type `docker compose up --build --force-recreate` to spin up the containers. 

After the containers are up you can use the command `docker compose exec django python manage.py migrate` for the database migrations and then `docker compose exec django python manage.py createsuperuser` to make your admin user. You can then go to the `/admin` panel and login with those credentials that you used to create the super user. 
