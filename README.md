# Kafka-Spark-Streaming-Tweets

Tweets relating to the term ``potus`` or ``biden`` are streamed from the Twitter API using the Tweepy module in Python to find the overall emotion of the tweet. The event stream is handled by a Kafka server that is created from a docker-compose file. Tweets are then processed through Spark Streaming with the Hugging Face [emotion-english-distilroberta-base](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base?text=Oh+Happy+Day) model being used to find the emotion of the tweet. The dataframe with ``tweet`` and ``emotion`` are then saved to a MongoDB database. 


![alt text](https://github.com/Raatid-Dilly/Kafka-Spark-Streaming-Tweets/blob/main/images/My%20First%20Board-2.jpg)

# Apache Kafka

Kafka is a streaming platform that:

- Publishes and subscribes to streams of records. Real-time streaming data pipelines can be built that reliably gets data between systems or applications
- Stores streams of records in a fault-tolerant way.
- Processes streams of records as they occur.
- Is ran as a cluster on one or more servers that can span multiple datacenters. The Kafka cluster stores streams of records in categories called topics. 

To send tweets a Kafka Producer is required to stream the records to a Kafka topic. Kafka services are ran in a [docker-compose file]() which is shown below. To run the docker-compose file ``cd`` into the file directory and execute ``docker-compose up`` in your CLI

```
version: "3"

services:
  zookeeper:
    image: wurstmeister/zookeeper
    hostname: zookeeper
    container_name: zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  kafka:
    image: wurstmeister/kafka
    hostname: kafka
    container_name: kafka
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ADVERTISED_HOST_NAME: localhost
      KAFKA_ZOOKEEPER_CONNECT: "zookeeper:2181"
```

# Twitter API and Tweepy

**Tweepy** - ``pip install tweepy``

**Twitter API** - A developer account from [Twitter API](https://developer.twitter.com/en/docs/twitter-api) is required. From there a ``Api Key``, ``Access Token``, and ``Bearer Token`` are needed.

Before sending tweets to the Kafka broker, they are cleaned to remove unwanted information such as links and mentions

```
def clean_tweet(tweet):
    tweet = tweet.text
    tweet = tweet.lower()
    tweet = re.sub("@[A-Za-z0-9_]+","", tweet)
    tweet = re.sub("#[A-Za-z0-9_]+","", tweet)
    tweet = re.sub(r"http\S+", '', tweet)
    tweet = re.sub('[()!?]', ' ', tweet)
    tweet = re.sub('\[.*?\]',' ', tweet)
    tweet = re.sub("[^a-z0-9'.]"," ", tweet)
    return tweet
```

Full script to stream tweets can be found [here]()

# Spark Streaming

Spark is used as a consumer to retrieve data from Kafka server inside which Kafka producers sent the real time tweets. For fetching the messages, Kafka consumers have to subscribe to the respective topic present inside the Kafka server. After being read by Spark, the messages are loaded into a Dataframe for transformation with EmoRoBERTa Text Classification to find the emotion of the tweet and then streamed to a MongoDB database.

**Reading from Kafka Server**:

```
tweets = spark.readStream \
    .format('kafka') \
    .option('kafka.bootstrap.servers', 'localhost:9092') \
    .option('subscribe', 'politics') \
    .option('startOffsets', 'earliest') \
    .option('failOnDataLoss', 'false') \
    .load()
 ```
 
 **Applying Hugging Face Model**
 
 ```
 MODEL_NAME = 'j-hartmann/emotion-english-distilroberta-base'
 sequenceClassifier_loaded = RoBertaForSequenceClassification.load("./{}_spark_nlp".format(MODEL_NAME))\
  .setInputCols(["document",'token'])\
  .setOutputCol("class")
 document_assembler = DocumentAssembler() \
    .setInputCol('text') \
    .setOutputCol('document') \
    .setCleanupMode('shrink')

tokenizer = Tokenizer() \
    .setInputCols(['document']) \
    .setOutputCol('token')

pipeline = Pipeline(stages=[
    document_assembler, 
    tokenizer,
    sequenceClassifier_loaded    
])

result = pipeline.fit(tweet_df).transform(tweet_df)
result = result.select("text", "class.result")
```
# MongoDB

![alt plot](https://github.com/Raatid-Dilly/Kafka-Spark-Streaming-Tweets/blob/main/images/mongoplot.jpg)

