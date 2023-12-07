#!/usr/bin/python3
import requests
from models.users import User


class Repository:
    def __init__(self, user, repo_name):
        self.user = user
        self.repo_name = repo_name
        self.repo_url = f'https://api.github.com/repos/{user.username}/{repo_name}'
        self.contributors_url = f'https://api.github.com/repos/{user.username}/{repo_name}/contributors'
        self.languages_url = f'https://api.github.com/repos/{user.username}/{repo_name}/languages'
        self.__repo_data = None
        self.__contributors = None
        self.__languages = None

    def fetch_repo_data(self, access_token):
        """ retrieves and returns repos of an authenticated user"""
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(self.repo_url, headers=headers)

        if response.status_code == 200:
            self.__repo_data = response.json()
            return True
        else:
            self.__repo_data = None
            return False

    def fetch_contributors(self, access_token):
        """ retieves the contributors for a repo"""
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(self.contributors_url, headers=headers)

        if response.status_code == 200:
            self.__contributors = response.json()
            return True
        else:
            self.__contributors = None
            return False
        
    def fetch_languages(self, access_token):
        """ retrieves all languages in a repo"""
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(self.languages_url, headers=headers)

        if response.status_code == 200:
            self.__languages = response.json()
            return True
        else:
            self.__languages = None
            return False
        
    def list_repo_details(self):
        return {
            'name': self.repo_name,
            'contributors': self.__contributors,
            'languages': self.__languages,
            'stars': self.__repo_data.get('stargazers_count', 'N/A') if self.__repo_data else 'N/A',
            'views': self.__repo_data.get('watchers_count', 'N/A') if self.__repo_data else 'N/A'  
        }