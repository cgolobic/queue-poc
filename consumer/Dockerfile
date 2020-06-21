FROM python:3.8.3-alpine
RUN apk update
RUN apk upgrade
RUN apk add bash
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chmod 755 ./wait-for-it.sh
CMD ["./wait-for-it.sh", "rabbitmq:5672", "--", "python", "consumer.py"]