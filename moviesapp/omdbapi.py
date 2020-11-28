from os import getenv
from requests import get as rget, ConnectionError
from libs.constants import (
    OMDB_API_KEY,
    OMDB_API_URL,
)


def _get_url(title: str) -> str:
    return f'{OMDB_API_URL}?t={title}&apikey={getenv(OMDB_API_KEY)}'


def fetch_omdbapi(title: str) -> dict:
    try:
        return rget(_get_url(title)).json()
    except ConnectionError:
        raise ConnectionError('asd')
