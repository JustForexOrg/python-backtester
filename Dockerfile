FROM python:3
COPY . /
CMD [ "python3", "./server.py" ]
