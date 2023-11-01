from kafka import KafkaConsumer
from confluent_kafka.admin import AdminClient, NewTopic
import pandas as pd
import json

bootstrap_servers = 'localhost:9092'
accounting_topic = 'accounting'
distribution_topic = 'distribution'
registration_topic = 'registration'

admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})

topic_1 = NewTopic(accounting_topic, num_partitions=1, replication_factor=1)
topic_2 = NewTopic(distribution_topic, num_partitions=1, replication_factor=1)
topic_3 = NewTopic(registration_topic, num_partitions=2, replication_factor=1)

admin_client.create_topics([topic_1, topic_2, topic_3])

consumer = KafkaConsumer(
    *[accounting_topic, distribution_topic, registration_topic],
    group_id='consumer_group',
    bootstrap_servers=[bootstrap_servers],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

sales_route = '../db/db_sales.csv'
restock_route = '../db/db_restock.csv'
users_route = '../db/db_users.csv'

while True:
    for msg in consumer:
        value = dict(msg.value)
        if msg.topic == accounting_topic:
            db_sales = pd.read_csv(sales_route)
            if len(db_sales[db_sales['id'] == value['id']]) > 0:
                #modificar
                row = db_sales[db_sales['id'] == value['id']]
                db_sales.loc[row.index[0], 'sales'] += 1
                db_sales.to_csv(sales_route, index=False)
            else:
                #añadir
                db_sales = pd.concat([db_sales, pd.DataFrame({'id': [value['id']], 'sales': [1]})], ignore_index=True)
                db_sales.to_csv(sales_route, index=False)
            print(f"Sale by {value['id']} stored in db...")
        elif msg.topic == distribution_topic:
            db_restock = pd.read_csv(restock_route)
            if len(db_restock[db_restock['id'] == value['id']]) > 0:
                #modificar
                row = db_restock[db_restock['id'] == value['id']]
                db_restock.loc[row.index[0], 'restocks'] += 1
                db_restock.to_csv(restock_route, index=False)
            else:
                #añadir
                db_restock = pd.concat([db_restock, pd.DataFrame({'id': [value['id']], 'restocks': [1]})], ignore_index=True)
                db_restock.to_csv(restock_route, index=False)
            print(f"Restock need by {value['id']} stored in db...")
        elif msg.topic == registration_topic:
            db_users = pd.read_csv(users_route)
            if msg.partition == 1:
                db_users = pd.concat([db_users, pd.DataFrame({'id': [value['id']], 'email': [value['email']], 'paid': [1]})], ignore_index=True)
                db_users.to_csv(users_route, index=False)
                print(f"New master with Paid {value['email']} stored in db...")  
            else:
                db_users = pd.concat([db_users, pd.DataFrame({'id': [value['id']], 'email': [value['email']], 'paid': [0]})], ignore_index=True)
                db_users.to_csv(users_route, index=False)
                print(f"New master {value['email']} stored in db...")    