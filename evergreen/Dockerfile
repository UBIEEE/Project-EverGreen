FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create testing enviroment
# ENV USER_EMAIL=testUser@buffalo.edu
# ENV USER_PASSWORD=password123!

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

