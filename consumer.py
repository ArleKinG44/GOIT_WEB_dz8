import pika
from models import Contact

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='contact_queue')

def send_email(contact_id):
    contact = Contact.objects.get(id=contact_id)
    print(f"Sending email to {contact.email}")

    contact.message_sent = True
    contact.save()

def callback(ch, method, properties, body):
    print(f"Received contact id: {body.decode()}")
    send_email(body.decode())

channel.basic_consume(queue='contact_queue', on_message_callback=callback, auto_ack=True)

print("Consumer is waiting for messages. To exit press CTRL+C")
channel.start_consuming()
