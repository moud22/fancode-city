import requests
import pytest

BASE_URL = 'http://jsonplaceholder.typicode.com/'

def get_users():
    response = requests.get(f'{BASE_URL}users')
    response.raise_for_status()
    return response.json()

def get_todos_for_user(user_id):
    response = requests.get(f'{BASE_URL}todos', params={'userId': user_id})
    response.raise_for_status()
    return response.json()

def is_fancode_city(user):
    lat = float(user['address']['geo']['lat'])
    lng = float(user['address']['geo']['lng'])
    return -40 <= lat <= 5 and 5 <= lng <= 100

def calculate_task_completion_percentage(todos):
    total_tasks = len(todos)
    completed_tasks = sum(1 for task in todos if task['completed'])
    if total_tasks == 0:
        return 0
    return (completed_tasks / total_tasks) * 100

@pytest.mark.parametrize('user', get_users())
def test_fancode_users_task_completion(user):
    if is_fancode_city(user):
        todos = get_todos_for_user(user['id'])
        completion_percentage = calculate_task_completion_percentage(todos)
        assert completion_percentage > 50, f"User {user['name']} has {completion_percentage}% tasks completed"
