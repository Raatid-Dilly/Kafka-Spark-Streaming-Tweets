import json
import os
from kafka import KafkaProducer

def serializer(message:str):
    """
    Create json string from message

    Args:
        message: text to be converted
    """
    return json.dumps(message).encode('utf-8')

def producer_send_tweet(message:str, topic_name:str):
    """
    Send tweet to Kafka server

    Args:
        message (str): message to be sent to Kafka broker
        topic_name (str): Kafka topic 
    """
    KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=serializer).send(topic=topic_name, value=message)

def create_topic(topic_name:str):
    """
    Create Kafka topic

    Args:
        topic_name: Kafka topic to be created
    """
    try:
        os.system(f"""docker exec -it kafka /bin/sh -c \
            "cd opt/kafka_2.13-2.8.1/bin \
            && kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 2 --topic {topic_name} && exit" 
             """)
    except: 
        print('Error')

def delete_topic(topic_name:str):
    """
    Delete Kafka topic

    Args:
        topic_name: Kafka topic to be deleted
    """
    try:
        os.system(f"""docker exec -it kafka /bin/sh -c \
            "cd opt/kafka_2.13-2.8.1/bin \
            && kafka-topics.sh --delete --zookeeper zookeeper:2181 --topic {topic_name} && exit" """)
    except:
        print('Error')