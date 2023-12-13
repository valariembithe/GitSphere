#!/usr/bin/python3
import requests


class User:
    def __init__(self, username):
        self.username = username
        self.api_url = f'https://api.github.com/users/{username}'
        self.repos_url = f'https://api.github.com/users/{username}/repos'
        self.__user_data = None
        self.__repositories = None

    def fetch_user_data(self, access_token):
        """ retrieves and returns info of an authenticated user"""
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(self.api_url, headers=headers)

        if response.status_code == 200:
            self.__user_data = response.json()
            return True
        else:
            self.__user_data = None
            return False
        
    def fetch_user_repositories(self, access_token):
        """ retrieves and returns repos of an authenticated user"""
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(self.repos_url, headers=headers)

        if response.status_code == 200:
            self.__repositories = response.json()
            return True
        else:
            self.__repositories = None
            return False 

    def get_user_data(self):
        return self.__user_data

    def get_user_repositories(self):
        return self.__repositories

    def is_valid_user(self):
        return self.__user_data is not None

    def is_valid_repositories(self):
        return self.__repositories is not None

    def get_user_name(self):
        return self.__user_data.get('name', 'N/A') if self.__user_data else 'N/A'
    
    def get_user_bio(self):
        return self.__user_data.get('bio', 'N/A') if self.__user_data else 'N/A'
    
    def get_user_followers(self):
        return self.__user_data.get('followers', 'N/A') if self.__user_data else 'N/A'
    
    def get_user_following(self):
        return self.__user_data.get('following', 'N/A') if self.__user_data else 'N/A'
    
    
