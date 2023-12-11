#!/usr/bin/python3


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
    return github.authorize(callback=url_for('authorize', _external=True))

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

@app.route('/user')
def get_authenticated_user():
    """ A function that retrieves the information of a user using username"""
    access_token = session.get('github_token')

    if access_token is None:
        return "Error: Github access token not found. Please Log in"
    headers = {'Authorization' : f'Bearer {access_token[0]}'}
    api_url = f'https://api.github.com/user'

    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        return render_template('user_profile.html', user_data=user_data)
    else:
         f'Error: Unable to fetch user data from GitHub API. Status code: {response.status_code}'

@app.route('/user/<username>')
def get_user_details(username):
    access_token = session.get('github_token')

    if access_token is None:
        return "Error: Github access token not found. Please Log in."
    headers = {'Authorization': f'Bearer {access_token[0]}'}
    api_url = f'https://api.github.com/user/{username}'
    
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        name = user_data.get('name', 'N/A')
        bio = user_data.get('bio', 'N/A')
        followers = user_data.get('followers', 'N/A')
        following = user_data.get('following', 'N/A')

        return render_template('user_data.html',
                               username=username,
                               name=name,
                               bio=bio,
                               followers=followers,
                               following=following)
    elif response.status_code == 404:
        return f'User "{username}" not found on GitHub.'
    else:
        return f'Error: Unable to fetch data from GitHub API. Status code: {response.status_code}'

    
@app.route('/user/<username>/repositories')
def get_user_repositories(username):
    access_token = session.get('github_token')

    if access_token is None:
        return "Error: Github access token not found. Please Log in."
    headers = {'Authorization': f'Bearer {access_token[0]}'}
    repos_api_url = f'https://api.github.com/user/{username}/repos'

    response = requests.get(repos_api_url, headers=headers)
    if response.status_code == 200:
        repositories = response.json()
        x =  repositories.get('user', 'N/A')
        return render_template('user_repos.html',
                               username=username,
                               repositories=repositories)
    else:
        return f'Error: Unable to fetch repositories from GitHub API. Status code: {response.status_code}'


@app.route('/repos/<owner>/<repo>/issues/<int:issue_number>', methods=['GET'])
def get_repository_issue(owner, repo, issue_number):
  
    access_token = session.get('github_token')

    if access_token is None:
        return "Error: Github access token not found. Please Log in."
    headers = {'Authorization': f'Bearer {access_token[0]}'}
    issues_api_url = f'https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}'

    response = requests.get(issues_api_url, headers=headers)
    if response.status_code == 200:
        issue_data = response.json()
        return render_template('issue_details.html', issue_data=issue_data)
    else:
        return f'Error: Unable to fetch issue from GitHub API. Status code: {response.status_code}'

@app.route('/repos/<owner>/<repo>/issues', methods=['POST'])
def create_repository_issue(owner, repo):

    access_token = session.get('github_token')

    if access_token is None:
        return "Error: Github access token not found. Please Log in."
    headers = {'Authorization': f'Bearer {access_token[0]}'}
    issues_api_url = f'https://api.github.com/repos/{owner}/{repo}/issues'
    
    data = {
        'title': request.form['title'],
        'body': request.form['body']
    } 

    response = requests.post(issues_api_url, headers=headers, json=data)
    if response.status_code == 201:
        return redirect(url_for('get_repository_issue', owner=owner, repo=repo))
    else:
        return f'Error: Unable to create issue on GitHub. Status code: {response.status_code}'
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
