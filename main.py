import json, requests
from confluent_kafka import Producer, Message
from confluent_kafka.cimpl import KafkaError
import time


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
    

if __name__ == '__main__':

    producer = Producer({'bootstrap.servers': 'localhost:9092'})

    bearer_token = input("Please provide the Twitter bearer token to authenticate your API request\n")
    url = 'https://api.twitter.com/2/tweets/search/recent?query=andjustlikethat&tweet.fields=created_at,lang&max_results=100'
    headers = {"Authorization": bearer_token}
    
    producer.poll(0)

    while True:
        data = get_data(url, headers)
        for record in data['data']:
            producer.produce('my_third_topic', json.dumps(record).encode('utf_8'), callback=print_delivery_report)
        producer.flush()
        print('Going to bed')
        time.sleep(60)

    

