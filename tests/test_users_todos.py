import requests
import pytest

BASE_URL = 'http://jsonplaceholder.typicode.com/'

def fetch_data(endpoint, params=None):
    try:
        response = requests.get(f'{BASE_URL}{endpoint}', params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"API request failed: {e}")

def get_users():
    return fetch_data('users')

def get_todos_for_user(user_id):
    return fetch_data('todos', {'userId': user_id})

def is_fancode_city(user):
    try:
        lat = float(user['address']['geo']['lat'])
        lng = float(user['address']['geo']['lng'])
        return -40 <= lat <= 5 and 5 <= lng <= 100
    except (KeyError, ValueError):
        return False

def calculate_task_completion_percentage(todos):
    total_tasks = len(todos)
    if total_tasks == 0:
        return 0
    completed_tasks = sum(1 for task in todos if task['completed'])
    return (completed_tasks / total_tasks) * 100

@pytest.fixture(scope="module")
def users():
    return get_users()

def test_fancode_users_task_completion(users):
    fancode_users = [user for user in users if is_fancode_city(user)]
    assert fancode_users, "No users found in FanCode City"

    for user in fancode_users:
        todos = get_todos_for_user(user['id'])
        completion_percentage = calculate_task_completion_percentage(todos)
        assert completion_percentage > 50, f"User {user['name']} has {completion_percentage}% of tasks completed"
