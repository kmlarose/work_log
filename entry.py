import datetime
import json


class Entry:
    """A log Entry - it has a name, time spent on task, and notes"""
    def __init__(self, task_name, time_spent, notes, date_created=None, **kwargs):
        self.task_name = task_name
        self.time_spent = time_spent
        self.notes = notes
        self.date_format = '%m-%d-%Y %H:%M'
        if date_created:
            self.date_created = datetime.datetime.strptime(date_created, self.date_format)
        else:
            self.date_created = datetime.datetime.now()
        self.date = self.date_created.strftime('%m-%d-%Y')

    def __str__(self):
        """Presents the Entry as a multi-line string"""
        template = ('Date: {}\n'
                    'Task Name: {}\n'
                    'Time Spent: {}\n'
                    'Notes: {}')
        return template.format(self.date_created, self.task_name, self.time_spent, self.notes)

    def convert_entry_to_json(self):
        """Represents the entry's attributes in a JSON string"""
        attributes = {'task_name': self.task_name,
                      'time_spent': self.time_spent,
                      'notes': self.notes,
                      'date_created': self.date_created.strftime(self.date_format)}
        return json.dumps(attributes)

    def save_new_entry(self):
        """Saves the Entry"""
        with open('work_log_entries.txt', 'a') as entries_log:
            entries_log.write(self.convert_entry_to_json()+'\n')

    # TODO-kml: ability to save changes to Entries
    def save(self):
        """Saves an Entry that already exists in the data file"""
        pass

    # TODO-kml: delete this entry from the data file
    def delete_from_data_file(self):
        pass
