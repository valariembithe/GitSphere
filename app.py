#!/usr/bin/python3
""" 
    This application uses Github OAuth Apps to create an app that uses GitHub API
    Params needed are client_ID, client_secret 
    Functions it can perform are retrieve user profile details, perform search,
    view repository details and statistics

"""

from flask import Flask, render_template, request, redirect, url_for, session
from flask_oauthlib.client import OAuth
import os
from dotenv import load_dotenv
import requests


load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24) #crypographic key that uses Flask to secure session cookies

oauth = OAuth(app)

#creates as an instance of OAuth remote app and specifies parameters
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
    """ Return welcome message """
    return "Welcome to GitSphere - Github Insights Web Service!"

@app.route('/login')
def login():
    """ 
        Redirects the user to GitHub for authentication.
        Github asks the end user to authorize/give permission to
        this application and prompts a login with GitHub
    """
    return github.authorize(callback=url_for('authorize', _external=True))

@app.route('/logout')
def logout():
    """  
        Logs the user out by clearing the session 
        and redirects to home page. 
    """
    session.pop('github_token', None)
    return redirect(url_for('home'))

@app.route('/login/authorize')
def authorize():
    """
        Callback route for handling the GitHub authorization response.
        If user authorizes the application, an access_token will be generated
        which is stored in variable 'github_token'
        Else if no response or access_token app will return an error message 'Access Denied'
        and redirects to home page
    """
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
    """
        The decorator specifies a function 
        that retrieves the GitHub access token from the session.
    """
    return session.get('github_token')

@app.route('/user')
def get_authenticated_user():
    """ 
        This route fetches information about the authenticated user using the GitHub API.
        Returns: 
                A template containing relevant info about the user eg: username, bio...
                Raises error if status code is not 200 OK
    """
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
    """
        Params: 
            username - a valid GitHub username
        Retrieves access_token to validated and returns error message if None
        Returns:  Information about a specific user.
                else: raises an error for 404 Not found
                handles other errors
    """

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
    """
        Params: 
            username - a valid GitHub username
        Includes access_token in headers and uses get method
        Returns: 
            Repositories for a specified user
    """
    access_token = session.get('github_token')

    if access_token is None:
        return "Error: Github access token not found. Please Log in."
    headers = {'Authorization': f'Bearer {access_token[0]}'}
    repos_api_url = f'https://api.github.com/user/{username}/repos'

    response = requests.get(repos_api_url, headers=headers)
    if response.status_code == 200:
        repositories = response.json()
        return render_template('user_repos.html',
                               username=username,
                               repositories=repositories)
    else:
        return f'Error: Unable to fetch repositories from GitHub API. Status code: {response.status_code}'


@app.route('/repos/<owner>/<repo>/issues/<int:issue_number>', methods=['GET'])
def get_repository_issue(owner, repo, issue_number):
    """
        Params:
            owner: Authenticated GitHub user and owner for specific repository
            repo: Target repository to retrieve issues
            issue_number: A specific issue identified by a unique id
        Returns: 
             Details for a specific issue in a repository.
    """
  
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
    """
        Params:
            owner: Authenticated GitHub user and owner for specific repository
            repo: Target repository to post an issues
        Returns:
            A template with the posted issue and the other issues for the repo
    """

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
