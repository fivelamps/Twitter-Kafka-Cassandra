import json, requests
from confluent_kafka import Producer, Message
from confluent_kafka.cimpl import KafkaError
import time
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
import re


def print_delivery_report(err: KafkaError, msg: Message) -> None:
    """
    Called once for each message produced to indicate delivery result.
    Triggered by poll()

    :param err: KafkaError
    :param msg: Message
    :return: void
    """
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def get_data(url, headers) -> dict:
    """
    Twitter API call.

    :param url: str
    :param headers: dict
    :return: dict
    """
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get the data (error {}): {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def get_sentiment(text):
    """
    Called to get sentiment value.

    :param text: str
    :return: float
    """
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)['compound']

def preprocess(record):
    """
    Called to clean incoming data.

    :param text: dict
    :return: dict
    """
    record['retweet_count'] = record['public_metrics']['retweet_count']
    record['reply_count'] = record['public_metrics']['reply_count']
    record['like_count'] = record['public_metrics']['like_count']
    record['quote_count'] = record['public_metrics']['quote_count']
    record.pop('public_metrics')
    record['text'] = re.sub('http\S+', '', record['text'])
    record['text'] = re.sub('@\w+', '', record['text'])
    record['text'] = re.sub('#', '', record['text'])
    record['text'] = re.sub('RT', '', record['text'])
    record['text'] = re.sub(':', '', record['text'])
    record['text'] = re.sub('  ', ' ', record['text'])
    record['text'] = re.sub('\n', '', record['text'])
    return record

 

if __name__ == '__main__':

    producer = Producer({'bootstrap.servers': 'localhost:9092'})

    bearer_token = input("Please provide the Twitter bearer token to authenticate your API request\n")
    url = 'https://api.twitter.com/2/tweets/search/recent?query=AmberHeard&tweet.fields=created_at,lang,public_metrics&max_results=100'
    headers = {"Authorization": bearer_token}
    
    producer.poll(0)

    while True:
        data = get_data(url, headers)
        for record in data['data']:
            if record['lang'] == 'en':
                preprocessed_record = preprocess(record)
                preprocessed_record['sentiment'] = get_sentiment(preprocessed_record['text'])
                producer.produce('amber_topic', json.dumps(preprocessed_record).encode('utf_8'), callback=print_delivery_report)

        producer.flush()
        print('Going to bed')
        time.sleep(2)



    

