import pika
from mongoengine import connect, Document, StringField, BooleanField
import json
import time

# Підключення до бази даних MongoDB
connect("mongodb+srv://akashyren77:<password>@whw8.ludjncu.mongodb.net/?retryWrites=true&w=majority")

# Модель контакту
class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    email_sent = BooleanField(default=False)

# Функція для імітації надсилання повідомлення по email
def send_email(contact_id):
    contact = Contact.objects.get(id=contact_id)
    print(f"Відправлено email на адресу {contact.email} для контакту {contact.full_name}")
    # Ваш код для надсилання повідомлення по email тут
    time.sleep(2)  # імітація відправки email
    contact.email_sent = True
    contact.save()

# Callback-функція для обробки повідомлень з черги
def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    send_email(contact_id)
    print("Повідомлення оброблено.")

# Підключення до черги RabbitMQ та отримання повідомлень
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_contacts_queue')
channel.basic_consume(queue='email_contacts_queue', on_message_callback=callback, auto_ack=True)

print("Чекаю на повідомлення. Щоб зупинити, натисніть Ctrl+C")
channel.start_consuming()
