import uuid
import hashlib
import requests
import json
from app import app
import urllib.parse
import string
import random

def create_api_key():
    """
    Create an API key from a random string
    :return: A sha1 hash
    """
    return hashlib.sha1(uuid.uuid4().hex.encode('utf-8')).hexdigest()


def create_unqiue_id():
    """
    Create a unique ID that is used by the nodes
    :return: A unqiue 16 character ID.
    """
    return uuid.uuid4().hex[:16]


def create_invite_code():
    """
    Create an invite code.
    :return: An invite code.
    """
    return str(uuid.uuid4())


def generate_password():
    # Just alphanumeric characters
    chars = string.ascii_letters + string.digits
    pwdSize = 20
    return ''.join((random.choice(chars)) for x in range(pwdSize))

def api_create(endpoint, data):
    data = {
        "page": "",
        "field": ""
    }
    r = requests.post(
        app.config['api_url'] + endpoint,
        headers=app.config['api_header'],
        data=json.dumps(data),
        verify=False)
    if r.status_code == 201:
        # If created then it returns the object data
        return json.loads(r.text)
    else:
        return {}


def api_update(endpoint, data):
    query = {"filters": [
        {
            "op": "eq",
            "name": "page",
            "val": ""
        }, {
            "op": "eq",
            "name": "field",
            "val": ""
        }]}
    data['q'] = query
    r = requests.patch(
        app.config['api_url'] + endpoint,
        headers=app.config['api_header'],
        data=json.dumps(data),
        verify=False)
    if r.status_code == 200:
        # if updated it returns the object data
        return json.loads(r.text)
    else:
        return {}


def __get_query(self, endpoint, query):
    r = requests.get(
        self.api_url + endpoint + '?q=' + urllib.parse.quote_plus(json.dumps(query)), verify=False)
    if r.status_code == 200:
        # If created then it returns the object data
        return json.loads(r.text).get('objects')
    else:
        return {}


