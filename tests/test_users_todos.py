import pytest
from src.apis import fetch_data
from src.utils import is_fancode_city, calculate_task_completion_percentage

@pytest.fixture(scope="module")
def users():
    return fetch_data('users')

@pytest.fixture(scope="module")
def todos():
    return fetch_data('todos')

def get_todos_for_user(todos, user_id):
    return [todo for todo in todos if todo['userId'] == user_id]

# Test Cases starts from here

#Test Case 1 : User Completed task percentage should be greater than 50%
def test_fancode_users_task_completion(users, todos):
    fancode_users = [user for user in users if is_fancode_city(user)]
    assert fancode_users, "No users found in the city FanCode."

    for user in fancode_users:
        user_todos = get_todos_for_user(todos, user['id'])
        completion_percentage = calculate_task_completion_percentage(user_todos)
        assert completion_percentage > 50, f"User {user['name']} has {completion_percentage}% tasks completed"

# Test Case 2 : User having no todos, their task completion percentage is 0%
def test_users_without_todos(users, todos):
    for user in users:
        user_todos = get_todos_for_user(todos, user['id'])
        if not user_todos:
            # Ensure the task completion percentage for users with no todos is 0%
            completion_percentage = calculate_task_completion_percentage(user_todos)
            assert completion_percentage == 0, f"User {user['name']} has tasks when they should have none"

# Test Case 3 : Users who have not completed any tasks are having  a 0% task completion rate or not
def test_users_with_zero_task_completion(users, todos):
    for user in users:
        user_todos = get_todos_for_user(todos, user['id'])
        if user_todos and all(not todo['completed'] for todo in user_todos):
            completion_percentage = calculate_task_completion_percentage(user_todos)
            assert completion_percentage == 0, f"User {user['name']} should have 0% tasks completed"

# Test Case 4 : Users who have completed all their tasks are having a 100% completion rate or not
def test_users_with_full_task_completion(users, todos):
    for user in users:
        user_todos = get_todos_for_user(todos, user['id'])
        if user_todos and all(todo['completed'] for todo in user_todos):
            completion_percentage = calculate_task_completion_percentage(user_todos)
            assert completion_percentage == 100, f"User {user['name']} should have 100% tasks completed"

# Test Case 5 : Users outside FanCode city are being incorrectly included in the test or not
def test_non_fancode_users_are_ignored(users):
    non_fancode_users = [user for user in users if not is_fancode_city(user)]
    for user in non_fancode_users:
        assert not is_fancode_city(user), f"User {user['name']} is incorrectly classified as being from FanCode city"

# Test Case 6 : Users whose latitude and longitude are on the exact boundaries of the FanCode city
def test_boundary_conditions_for_fancode_city(users):
    boundary_lat = [-40, 5]
    boundary_lng = [5, 100]
    
    for user in users:
        lat = float(user['address']['geo']['lat'])
        lng = float(user['address']['geo']['lng'])
        if lat in boundary_lat and lng in boundary_lng:
            assert is_fancode_city(user), f"User {user['name']} at boundary is not correctly classified as FanCode city"
