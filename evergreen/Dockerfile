FROM python:3.10

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
SHELL [ "poetry", "run" ]
CMD [ "python3","manage.py","runserver","0.0.0.0:8080"]

