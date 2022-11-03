FROM python:3.8-slim-buster

COPY ./requirments.txt /app/requirments.txt

WORKDIR /app

RUN pip3 install -r requirments.txt

COPY . .

ENTRYPOINT [ "gunicorn", "-w", "4", "-b", "0.0.0.0:${PORT}","run:app"]