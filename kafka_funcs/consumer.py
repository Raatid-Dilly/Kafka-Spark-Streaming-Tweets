import json
from kafka import KafkaConsumer

def consume_message(topic):
    consumer = KafkaConsumer(topics=topic, bootstrap_servers='localhost:9092', auto_offset_reset='earliest')

    for message in consumer:
        print(json.loads(message.value))


    
    