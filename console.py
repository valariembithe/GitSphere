#!/usr/bin/python3
""" Creating  a Command Line Interface with client_id"""

from json import JSONDecoder
from json import JSONEncoder
from json import JSONDecodeError
import json
import sys
from urllib.parse import urlencode
from urllib.request import urlopen, Request 


def generate_authorization_url(client_id, redirect_uri, state):
    """ Generates a authorization url"""
    base_url = "https://github.com/login/oauth/authorize"
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "state": state
    }
    auth_url = f"{base_url}?{urlencode(params)}"
    return auth_url

client_id = "Iv1.84422fa8f410b93b"
state = "creatingagithubapp"
redirect_uri = "https://github.com/valariembithe/Git_Spy_v2"

authorization_url = generate_authorization_url(client_id, redirect_uri, state)
print(authorization_url)


def generate_access_token(client_id, client_secret, redirect_uri, code):
    """ Generates user access token to use during making API requests on 
        behalf of a user"""
    url = "https://github.com/login/oauth/access_token"
    data = {
        "client_id": client_id,
        "client-secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri
    }
    headers = {
        "Accept": "application/json"
    }

    req = Request(url, urlencode(data).encode(), headers)
    response = urlopen(req).read().decode()

    try:
        response.status_code()
        parsed_response = response.json()

        if "access_token" in parsed_response:
            return parsed_response
        else:
            raise ValueError("Response does not contain a valid access token.")
    except Request.HTTPError as http_err:
        raise http_err
    
client_id = "Iv1.84422fa8f410b93b"
client_secret = "8bce57a36f74e7d208ac040b67df5db1e3bc3f36"
redirect_uri = "https://github.com/valariembithe/Git_Spy_v2"
code = ""

token_response = generate_access_token(client_id, client_secret, redirect_uri, code)
print(token_response)

def parse_response(response):
    """ Parse a response and handle errors"""
    try:
        if (response.status_code == 200 or response.status_code == 201):
            return json.parse(response.body)
    except json.JSONDecodeError as json_err:
        print(f"JSON Decode Error: {json_err}")
        print(f"Status code: {response.status_code}")
        print(f"Reponse body: {response.body}")
        sys.exit(1)

def help():
    print("Usage: console <help>")

def main():
    if len(sys.argv) < 2:
        print("Usage: python console.py <command>")
        sys.exit(1)

    command = sys.argv[1]
    if command == 'help':
        help()
    elif command == 'login':
        print("`login` isnot defined")
    elif command == 'whoami':
        print("`whoami` is not defined")
    else:
        print("Unknown command {}".format(command))
 

if __name__ == "__main__":
    main()