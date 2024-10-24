#can change python version if we want...just put 3.8 since my computer runs 3.9.13
# TODO: change requirements.txt to poetry
FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /root
COPY pyproject.toml .
RUN pip3 install poetry 
RUN poetry config virtualenvs.create false --local


RUN poetry install 
COPY . .

EXPOSE 8080

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait
RUN ["/wait"]

SHELL [ "poetry", "run" ]

# RUN [ "python3","manage.py","makemigrations", "--no-input"]
# RUN [ "python3","manage.py","migrate", "--no-input"]

CMD [ "python3","manage.py","runserver","0.0.0.0:8080"]

