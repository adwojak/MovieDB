from django.test import TestCase
from rest_framework.test import RequestsClient


class MoviesAppTexts(TestCase):

    BASE = 'http://localhost:8000'
    REGISTER = f'{BASE}/register/'
    TOKEN = f'{BASE}/token/'
    MOVIES = f'{BASE}/movies/'
    user_data = {'username': 'username', 'password': 'password'}

    def get_authorization_header(self, client):
        access_token = self.get_access_token(client)
        return {'Authorization': f'Bearer {access_token}'}

    def register_user(self, client):
        return client.post(self.REGISTER, json=self.user_data).json()

    def generate_token(self, client):
        return client.post(self.TOKEN, json=self.user_data).json()

    def get_access_token(self, client):
        self.register_user(client)
        return self.generate_token(client)['access']

    def test_register(self):
        client = RequestsClient()
        response = client.post(self.REGISTER, json=self.user_data)
        assert response.status_code == 201

    def test_generate_token(self):
        client = RequestsClient()
        self.register_user(client)
        token = self.generate_token(client)
        assert 'refresh' in token
        assert 'access' in token

    def test_movies_no_token_provided(self):
        client = RequestsClient()
        response = client.get(self.MOVIES)
        assert response.status_code == 401

    def test_get_empty_movies(self):
        client = RequestsClient()
        response = client.get(self.MOVIES, headers=self.get_authorization_header(client))
        assert response.status_code == 200
        assert len(response.json()['results']) == 0

    def test_movie_invalid_omdbapi_key(self):
        client = RequestsClient()
        response = client.post(self.MOVIES, json={'title': 'Matrix'}, headers=self.get_authorization_header(client))
        assert response.status_code == 400
