from kafka import KafkaProducer
from json import dumps

bootstrap_servers = 'localhost:9092'
accounting_topic = 'accounting'
distribution_topic = 'distribution'
registration_topic = 'registration'

producer = KafkaProducer(bootstrap_servers=[bootstrap_servers])

def send_sale (ID):
    topic = accounting_topic
    message = {
        'id' : ID
    }
    json_message = dumps(message).encode('utf-8')
    producer.send(topic, json_message)
    print('Registered sale sent by: ', ID)

def send_no_stock (ID):
    topic = distribution_topic
    message = {
        'id' : ID
    }
    json_message = dumps(message).encode('utf-8')
    producer.send(topic, json_message)
    print('Registered no stock sent by: ', ID)
    
def send_registration (ID, isPaid):
    topic = registration_topic
    message = {
        'id' : ID,
        'email' : ID+'@mail.com' 
    }
    json_message = dumps(message).encode('utf-8')
    
    if isPaid:
        producer.send(topic, json_message, partition=1)
        print('Registered registration sent with Paid by: ', ID)
    else:
        producer.send(topic, json_message, partition=0)
        print('Registered registration sent with no Paid by: ', ID)