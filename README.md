# Kafka-Spark-Streaming-Tweets

Tweets relating to the term ``potus`` or ``biden`` are streamed from the Twitter API using the Tweepy module in Python. The event stream is handled by a Kafka server that is created from a docker-compose file. Tweets are then processed through Spark Streaming with Hugging Face [emotion-english-distilroberta-base](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base?text=Oh+Happy+Day) being used to find the emotion of the tweet. The dataframe with ``tweet`` and ``emotion`` are then saved to a MongoDB database. 


![alt text](https://github.com/Raatid-Dilly/Kafka-Spark-Streaming-Tweets/blob/main/images/My%20First%20Board-2.jpg)

# Apache Kafka

Kafka is a streaming platform that:

- Publishes and subscribes to streams of records. Real-time streaming data pipelines can be built that reliably gets data between systems or applications
- Stores streams of records in a fault-tolerant way.
- Processes streams of records as they occur.
- Is ran as a cluster on one or more servers that can span multiple datacenters. The Kafka cluster stores streams of records in categories called topics. 

To send tweets a Kafka Producer is required to stream the records to a Kafka topic. The producer script is shown below:

Kafka services are ran in a docker-compose file shown below. To run the docker-compose file ``cd`` into the file directory and execute ``docker-compose up`` in your CLI

# Twitter API and Tweepy

**Tweepy** - ``pip install tweepy``

**Twitter API** - A developer account from [Twitter API](https://developer.twitter.com/en/docs/twitter-api) is required. 


Script to stream tweets can be found [here]()

# Spark Streaming

Spark is used as a consumer to retrieve data from Kafka server inside which Kafka producers sent the real time tweets. For fetching the messages, Kafka consumers have to subscribe to the respective topic present inside the Kafka server. After being read by Spark, the messages are loaded into a Dataframe for transformation with EmoRoBERTa Text Classification to find the emotion of the tweet and then streamed to a MongoDB database.

Reading from Kafka Server:



# MongoDB



