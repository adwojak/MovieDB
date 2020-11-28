from os import getenv
from requests import get as rget, ConnectionError
from libs.constants import (
    OMDB_API_KEY,
    OMDB_API_URL,
)
from libs.errors import OMDBAPI_UNAVAILABLE
from libs.utils import to_snake_case

keys_for_manual_override = {
    'imdbID': 'imdb_id'
}


def _get_url(title: str) -> str:
    return f'{OMDB_API_URL}?t={title}&apikey={getenv(OMDB_API_KEY)}'


def _remove_na(response):
    response_without_na = response.copy()
    for key, value in response.items():
        if value == 'N/A':
            response_without_na.pop(key)
    return response_without_na


def fetch_omdbapi(title: str, remove_na: bool = True) -> dict:
    try:
        response = rget(_get_url(title)).json()
        if not response['Response']:
            return response['Error']
        response.pop('Response')
        if remove_na:
            response = _remove_na(response)
        return to_snake_case(response, keys_for_manual_override)
    except ConnectionError:
        raise ConnectionError(OMDBAPI_UNAVAILABLE)
