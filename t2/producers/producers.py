from kafka import KafkaProducer
from confluent_kafka.admin import AdminClient, NewTopic
from json import dumps

bootstrap_servers = 'localhost:9092'
accounting_topic = 'accounting'
distribution_topic = 'distribution'
registration_topic = 'registration'

admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})

topic_1 = NewTopic(accounting_topic, num_partitions=1, replication_factor=1)
topic_2 = NewTopic(distribution_topic, num_partitions=1, replication_factor=1)
topic_3 = NewTopic(registration_topic, num_partitions=2, replication_factor=1)

admin_client.create_topics([topic_1, topic_2, topic_3])

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
        'email' : ID+'@gmail.com' 
    }
    json_message = dumps(message).encode('utf-8')
    
    if isPaid:
        producer.send(topic, json_message, partition=1)
        print('Registered registration sent with Paid by: ', ID)
    else:
        producer.send(topic, json_message, partition=0)
        print('Registered registration sent with no Paid by: ', ID)