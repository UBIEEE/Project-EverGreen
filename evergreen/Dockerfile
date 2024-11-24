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

SHELL [ "poetry", "run" ]
RUN [ "python3","manage.py","makemigrations" ]

ENTRYPOINT [ "./docker-entrypoint.sh" ]
#CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8080" ]
CMD ["daphne", "-b", "0.0.0.0", "-p", "8080", "evergreen.asgi:application"]
