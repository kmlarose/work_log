import csv
import datetime
import random
import string


class Entry:
    """A log Entry - it has a name, time spent on task, and notes"""
    def __init__(self, task_name, time_spent, notes, date_created=None, unique_id=None, **kwargs):
        self.task_name = task_name
        self.time_spent = int(time_spent)
        self.notes = notes
        self.date_format = '%m-%d-%Y %H:%M'
        self.fieldnames = ['unique_id', 'task_name', 'time_spent', 'notes', 'date_created']
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

    def save_new_entry(self):
        """Saves the Entry"""
        with open('work_log_entries.csv', 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames, delimiter='|')
            writer.writerow({'unique_id': self.unique_id,
                             'task_name': self.task_name,
                             'time_spent': self.time_spent,
                             'notes': self.notes,
                             'date_created': self.date_created.strftime(self.date_format)})

    def save(self):
        """Save changes to an existing Entry"""
        self.delete_from_data_file()
        self.save_new_entry()

    def delete_from_data_file(self):
        """Deletes an Entry from the data file"""
        all_entries = []
        with open('work_log_entries.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='|')
            for row in reader:
                all_entries.append(row)
        # write all the entries except for the one to be deleted
        with open('work_log_entries.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames, delimiter='|')
            writer.writeheader()
            for entry in all_entries:
                if entry['unique_id'] != self.unique_id:
                    writer.writerow(entry)

    @staticmethod
    def get_unique_id():
        """Assigns a unique ID for an Entry"""
        unique_ids = []
        # find IDs that have been already been used
        with open('work_log_entries.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='|')
            for row in reader:
                unique_ids.append(row['unique_id'])

        # generate a random ID and make sure it hasn't been used already
        while True:
            unique_id = random.sample(string.printable[:95], 10)
            if unique_id not in unique_ids:
                break
        return ''.join(unique_id)
