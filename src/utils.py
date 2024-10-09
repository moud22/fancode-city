def fancode_city(user):
    try:
        lat = float(user['address']['geo']['lat'])
        lng = float(user['address']['geo']['lng'])
        return -40 <= lat <= 5 and 5 <= lng <= 100
    except (KeyError, ValueError):
        return False

def task_completion_rate(todos):
    total_tasks = len(todos)
    if total_tasks == 0:
        return 0
    completed_tasks = sum(1 for task in todos if task['completed'])
    return (completed_tasks / total_tasks) * 100
