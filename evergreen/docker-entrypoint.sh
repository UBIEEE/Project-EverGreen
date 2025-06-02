#!/bin/bash

python3 manage.py migrate
echo 
exec "$@"
