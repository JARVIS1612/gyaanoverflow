FROM python:3.8-slim-buster

COPY ./requirments.txt /app/requirments.txt

WORKDIR /app

RUN pip3 install -r requirments.txt

COPY . .

ARG PORT=8004
ENV PORT=$PORT
#start server
EXPOSE ${PORT}

ENTRYPOINT [ "gunicorn", "-w", "4", "-b", "0.0.0.0:'${PORT}'","wsgi:app" ]
