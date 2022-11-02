FROM python:3.8-slim-buster

COPY ./requirments.txt /app/requirments.txt

WORKDIR /app

RUN pip3 install -r requirments.txt

COPY . .

CMD ["export", "FLASK_RUN_PORT=8800"]

CMD [ "flask", "--app", "run.py", "run", "--host=0.0.0.0"]
