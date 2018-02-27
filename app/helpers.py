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


def create_unique_id():
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


def gen_api_header():
    myhead = dict()
    myhead['Content-Type'] = 'application/json'
    myhead['Authorization'] = 'Token {}'.format(app.config['API_KEY'])
    myhead['Authorization-Node'] = app.config['API_NODE']
    return myhead


def generate_password():
    # Just alphanumeric characters
    chars = string.ascii_letters + string.digits
    pwdsize = 20
    return ''.join((random.choice(chars)) for x in range(pwdsize))


def api_create(endpoint, data):
    r = requests.post(
        app.config['API_URL'] + endpoint,
        headers=gen_api_header(),
        data=json.dumps(data),
        verify=False)
    if r.status_code == 201:
        # If created then it returns the object data
        return json.loads(r.text)
    else:
        return {}


def api_delete(endpoint, id_):
    r = requests.delete(
        app.config['API_URL'] + endpoint + '/' + id_,
        headers=gen_api_header(),
        verify=False)
    if r.status_code == 204:
        return True
    else:
        return False


def api_update(endpoint, data):
    r = requests.patch(
        app.config['API_URL'] + endpoint,
        headers=gen_api_header(),
        data=json.dumps(data),
        verify=False)
    if r.status_code == 200:
        # if updated it returns the object data
        return json.loads(r.text)
    else:
        return {}


def api_get(endpoint, query):
    r = requests.get(
        app.config['API_URL'] + endpoint + '?q=' + urllib.parse.quote_plus(json.dumps(query)),
        headers=gen_api_header(),
        verify=False)
    if r.status_code == 200:
        # If created then it returns the object data
        return json.loads(r.text).get('objects')
    else:
        return {}
