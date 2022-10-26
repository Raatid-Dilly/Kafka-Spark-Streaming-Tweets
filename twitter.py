import tweepy
import json
import re
from datetime import datetime
from kafka_funcs.helper_functions import producer_send_tweet, create_topic, delete_topic

with open('/Volumes/SANDISK/Twitter/credentials.json', 'r') as f:
    cred = json.load(f)

api_key = cred['API_Key']
api_key_secret = cred['API_Key_Secret']
bearer_token = cred['Bearer_Token']
access_token = cred['Access_Token']
access_token_secret = cred['Access_Token_Secret']

#Authentication
client = tweepy.Client(bearer_token, api_key, api_key_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
api = tweepy.API(auth)

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
    

rules = '(biden OR potus) lang:en -is:retweet'

class MyStreamListener(tweepy.StreamingClient):
    def on_connect(self):
        print('Connected')

    def on_tweet(self, tweet):    
        if tweet.referenced_tweets == None:
            try:
                tweet = clean_tweet(tweet)
                producer_send_tweet(tweet, topic_name='politics')
                now = datetime.now()
                print(f"{now.hour}:{now.minute}:{now.second} sending tweet")
            except BaseException as e:
                print('Error', e)
        return True

    def on_errors(self, errors):
        print(errors)
        return True

if __name__ == "__main__":
    
    stream = MyStreamListener(bearer_token=bearer_token, wait_on_rate_limit=True)
    stream.add_rules(tweepy.StreamRule(rules))
    stream.filter(tweet_fields=['referenced_tweets'])
