""" Create an application that handles full-ledged login
    authenticates users with Github, 
    retrieve info about a user and their repositories
"""


from flask import Flask, render_template, request, redirect, url_for, session
from flask_oauthlib.client import OAuth
import os
from dotenv import load_dotenv
from urllib.parse import quote as url_quote
import requests


load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24) #crypographic key that uses Flask to secure session cookies

oauth = OAuth(app)

#creates as an instance of Oauth remote app and specifies parameters
github = oauth.remote_app(
    'github',
    consumer_key=os.environ.get('GITHUB_CLIENT_ID'),
    consumer_secret=os.environ.get('GITHUB_CLIENT_SECRET'),
    request_token_params={'scope': 'user'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)

@app.route('/')
def home():
    """ Landing page """
    return "Welcome to Github Web Service!"

@app.route('/login')
def login():
    """ Login page with Github using OAuth """
    return github.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    """ logout of app """
    session.pop('github_token', None)
    return redirect(url_for('home'))

@app.route('/login/authorize')
def authorize():
    response = github.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
                request.args['error_reason'],
                request.args['error_description']
        )
    
    session['github_token'] = (response['access_token'], '')

    return redirect(url_for('home'))

@github.tokengetter
def get_github_auth_token():
    return session.get('github_token')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    app.run()
