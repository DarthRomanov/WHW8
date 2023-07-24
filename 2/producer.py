import pika
from mongoengine import connect, Document, StringField, BooleanField
import json
from faker import Faker

# Підключення до бази даних MongoDB
connect("mongodb+srv://akashyren77:<password>@whw8.ludjncu.mongodb.net/?retryWrites=true&w=majority")

# Модель контакту
class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    email_sent = BooleanField(default=False)

# Функція для генерації фейкових контактів та запису їх у базу даних
def generate_fake_contacts(num_contacts):
    fake = Faker()
    for _ in range(num_contacts):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
            email_sent=False
        )
        contact.save()

# Функція для створення повідомлень та їх відправки до черги RabbitMQ
def send_messages_to_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='email_contacts_queue')

    contacts = Contact.objects(email_sent=False)
    for contact in contacts:
        message = {'contact_id': str(contact.id)}
        channel.basic_publish(exchange='', routing_key='email_contacts_queue', body=json.dumps(message))
        print(f"Повідомлення для контакту {contact.full_name} ({contact.email}) додано до черги.")
        contact.email_sent = True
        contact.save()

    connection.close()

if __name__ == "__main__":
    num_fake_contacts = 10
    generate_fake_contacts(num_fake_contacts)
    send_messages_to_queue()
