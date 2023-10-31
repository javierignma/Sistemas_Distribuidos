FROM python:3.9

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN pip install -r requirements.txt

EXPOSE 9092

CMD ["sh", "-c", "while true; do sleep 1000; done"]