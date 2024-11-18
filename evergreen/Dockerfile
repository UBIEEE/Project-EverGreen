FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /root
COPY pyproject.toml .
RUN pip3 install poetry 

RUN poetry config virtualenvs.create false --local

# RUN apt-get update && apt-get install -y nginx
# RUN rm /etc/nginx/conf.d/default.conf

RUN poetry install 

COPY . .

EXPOSE 8080

# CMD ["nginx", "-g"]

SHELL [ "poetry", "run" ]
RUN [ "python3","manage.py","makemigrations" ]

ENTRYPOINT [ "./docker-entrypoint.sh" ]
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8080" ]