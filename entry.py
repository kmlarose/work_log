class Entry:
    """A log entry - it has a name, time spent on task, and notes"""
    def __init__(self, task_name, time_spent, notes):
        self.task_name = task_name
        self.time_spent = time_spent
        self.notes = notes
