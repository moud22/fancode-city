import requests

BASE_URL = 'http://jsonplaceholder.typicode.com/'

def fetch_data(endpoint, params=None):
    try:
        response = requests.get(f'{BASE_URL}{endpoint}', params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"API request failed: {e}")
