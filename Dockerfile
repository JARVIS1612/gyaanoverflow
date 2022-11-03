FROM python:3.8-slim-buster

COPY ./requirments.txt /app/requirments.txt

ARG PORT

WORKDIR /app

RUN pip3 install -r requirments.txt

COPY . .

CMD [ "gunicorn", "-w", "-b", "0.0.0.0:${PORT}","run:app"]