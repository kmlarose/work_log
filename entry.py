import datetime
import json
import random
import string


class Entry:
    """A log Entry - it has a name, time spent on task, and notes"""
    def __init__(self, task_name, time_spent, notes, date_created=None, unique_id=None, **kwargs):
        self.task_name = task_name
        self.time_spent = time_spent
        self.notes = notes
        self.date_format = '%m-%d-%Y %H:%M'
        if date_created:
            self.date_created = datetime.datetime.strptime(date_created, self.date_format)
        else:
            self.date_created = datetime.datetime.now()
        self.date = self.date_created.strftime('%m-%d-%Y')
        if unique_id:
            self.unique_id = unique_id
        else:
            self.unique_id = Entry.get_unique_id()

    def __str__(self):
        """Presents the Entry as a multi-line string"""
        template = ('Date: {}\n'
                    'Task Name: {}\n'
                    'Time Spent: {}\n'
                    'Notes: {}')
        return template.format(self.date_created, self.task_name, self.time_spent, self.notes)

    def convert_entry_to_json(self):
        """Represents the entry's attributes in a JSON string"""
        attributes = {'unique_id': self.unique_id,
                      'task_name': self.task_name,
                      'time_spent': self.time_spent,
                      'notes': self.notes,
                      'date_created': self.date_created.strftime(self.date_format)}
        return json.dumps(attributes)

    def save_new_entry(self):
        """Saves the Entry"""
        with open('work_log_entries.txt', 'a') as entries_log:
            entries_log.write(self.convert_entry_to_json()+'\n')

    def save(self):
        """Save changes to an existing Entry"""
        self.delete_from_data_file()
        self.save_new_entry()

    def delete_from_data_file(self):
        """Deletes an Entry from the data file"""
        all_entries = []
        # read all the saved entries
        with open('work_log_entries.txt', 'r') as entries_log:
            for line in entries_log:
                all_entries.append(json.loads(line[:-1]))
        # write all the entries except for the one to be deleted
        with open('work_log_entries.txt', 'w') as entries_log:
            for entry in all_entries:
                if entry['unique_id'] != self.unique_id:
                    entries_log.write(json.dumps(entry)+'\n')

    @staticmethod
    def get_unique_id():
        """Assigns a unique ID for an Entry"""
        unique_ids = []
        # find IDs that have been already been used
        with open('work_log_entries.txt', 'r') as entries_log:
            for line in entries_log:
                entry = json.loads(line[:-1])
                unique_ids.append(entry['unique_id'])
        # generate a random ID and make sure it hasn't been used already
        while True:
            unique_id = random.sample(string.printable[:95], 10)
            if unique_id not in unique_ids:
                break
        return ''.join(unique_id)
