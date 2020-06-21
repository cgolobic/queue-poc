import pika
import json
import time

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    while True:
        payload = json.dumps({ 'numerator': 10, 'denominator': 3 })
        channel.basic_publish(exchange='messages.fanout', routing_key='', body=payload)
        time.sleep(0.5)


if __name__ == "__main__":
    main()