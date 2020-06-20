import pika

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.basic_publish(exchange='messages.fanout', routing_key='', body='hello world')
    print('sent message to fanout queue')


if __name__ == "__main__":
    main()