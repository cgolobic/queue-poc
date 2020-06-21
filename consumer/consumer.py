import pika
import time
import random
import requests

def callback(ch, method, properties, body):
    r = random.random()
    denominator = (0, r * 10)[r < 0.5]
    response = requests.post('http://api:5000/calculate', json={
        'numerator': 5,
        'denominator': denominator
    })
    time.sleep(0.1)  #<< causes unacked messages if too high (slow consumer).  Use QoS to buffer messages...
    if response.status_code == 200:
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.basic_consume(queue='messages', on_message_callback=callback)
    channel.start_consuming()

if __name__ == "__main__":
    main()