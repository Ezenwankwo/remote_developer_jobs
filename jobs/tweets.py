import os
import requests
import json
import dateutil
from dateutil import parser
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth

from .models import Job

consumer_key = "KMY8GeQwSyETxlOXjvMEm9f05"  # Add your API key here
consumer_secret = (
    "BEiiAllNdi7b7bYW5CCfEhtPLbS3owKHwXz30Sq0doP1WFoe4a"  # Add your API secret key here
)

stream_url = "https://api.twitter.com/labs/1/tweets/stream/filter"
rules_url = "https://api.twitter.com/labs/1/tweets/stream/filter/rules"

sample_rules = [
    {"value": "remote developer", "tag": "remote developer"},
    {"value": "remote python", "tag": "python developer"},
]

# Gets a bearer token
class BearerTokenAuth(AuthBase):
    def __init__(self, consumer_key, consumer_secret):
        self.bearer_token_url = "https://api.twitter.com/oauth2/token"
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.bearer_token = self.get_bearer_token()

    def get_bearer_token(self):
        response = requests.post(
            self.bearer_token_url,
            auth=(self.consumer_key, self.consumer_secret),
            data={"grant_type": "client_credentials"},
            headers={"User-Agent": "TwitterDevFilteredStreamQuickStartPython"},
        )

        if response.status_code is not 200:
            raise Exception(
                f"Cannot get a Bearer token (HTTP %d): %s"
                % (response.status_code, response.text)
            )

        body = response.json()
        return body["access_token"]

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer %s" % self.bearer_token
        r.headers["User-Agent"] = "TwitterDevFilteredStreamQuickStartPython"
        return r


def get_all_rules(auth):
    response = requests.get(rules_url, auth=auth)

    if response.status_code is not 200:
        raise Exception(
            f"Cannot get rules (HTTP %d): %s" % (response.status_code, response.text)
        )

    return response.json()


def delete_all_rules(rules, auth):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))

    payload = {"delete": {"ids": ids}}

    response = requests.post(rules_url, auth=auth, json=payload)

    if response.status_code is not 200:
        raise Exception(
            f"Cannot delete rules (HTTP %d): %s" % (response.status_code, response.text)
        )


def set_rules(rules, auth):
    if rules is None:
        return

    payload = {"add": rules}

    response = requests.post(rules_url, auth=auth, json=payload)

    if response.status_code is not 201:
        raise Exception(
            f"Cannot create rules (HTTP %d): %s" % (response.status_code, response.text)
        )


def stream_connect(auth):
    response = requests.get(stream_url, auth=auth, stream=True)
    for response_line in response.iter_lines():
        if response_line:
            job_tweet = json.loads(response_line)
            tweet_id = job_tweet["data"]["id"]
            tweet_time = job_tweet["data"]["created_at"]
            tweet_time = parser.isoparse(tweet_time)
            tweet_text = job_tweet["data"]["text"]
            job = Job(tweet_id=tweet_id, created_at=tweet_time, text=tweet_text)
            job.save()


bearer_token = BearerTokenAuth(consumer_key, consumer_secret)


def setup_rules(auth):
    current_rules = get_all_rules(auth)
    delete_all_rules(current_rules, auth)
    set_rules(sample_rules, auth)


# Comment this line if you already setup rules and want to keep them
# setup_rules(bearer_token)

