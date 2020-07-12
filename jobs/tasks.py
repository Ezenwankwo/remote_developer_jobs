import time

from .tweets import setup_rules, stream_connect, bearer_token


# @shared_task
def get_tweets():
    """this function will get tweets from the twitter api 
    and save them to the database"""
    setup_rules(bearer_token)
    # Listen to the stream.
    # This reconnection logic will attempt to reconnect when a disconnection is detected.
    # To avoid rate limites, this logic implements exponential backoff, so the wait time
    # will increase if the client cannot reconnect to the stream.
    timeout = 0
    while True:
        stream_connect(bearer_token)
        time.sleep(2 ** timeout)
        timeout += 1
