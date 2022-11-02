FROM python:3.8-slim-buster

COPY ./requirments.txt /app/requirments.txt

WORKDIR /app

RUN pip3 install -r requirments.txt

COPY . .

CMD [ "flask", "--app", "run.py", "run", "--host=0.0.0.0", "--port=$PORT"]
