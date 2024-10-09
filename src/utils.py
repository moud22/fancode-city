def is_fancode_city(user):
    """Determines if a user belongs to FanCode city based on latitude and longitude."""
    try:
        lat = float(user['address']['geo']['lat'])
        lng = float(user['address']['geo']['lng'])
        return -40 <= lat <= 5 and 5 <= lng <= 100
    except (KeyError, ValueError):
        return False

def calculate_task_completion_percentage(todos):
    """Calculates the percentage of completed tasks for a user's todos."""
    total_tasks = len(todos)
    if total_tasks == 0:
        return 0
    completed_tasks = sum(1 for task in todos if task['completed'])
    return (completed_tasks / total_tasks) * 100
