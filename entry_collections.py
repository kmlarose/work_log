import csv
import datetime
import re

from entry import Entry


class EntryCollection:
    """A collection of all the log Entries from the data file"""

    def __init__(self):
        self.entries = []
        # import all of the entry data as dictionaries
        saved_data = []
        with open('work_log_entries.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='|')
            for row in reader:
                saved_data.append(row)
        # use those as **kwargs to instantiate Entries
        [self.entries.append(Entry(**data)) for data in saved_data]

    def __len__(self):
        return len(self.entries)

    def __iter__(self):
        yield from self.entries

    def __getitem__(self, item):
        return self.entries.__getitem__(item)

    def filter_by_date(self, date):
        """Filters the collection for only Entries of a certain date"""
        date = date.strftime('%m-%d-%Y')
        while any(entry.date != date for entry in self.entries):
            for entry in self.entries:
                if entry.date != date:
                    self.entries.remove(entry)
        return self.entries

    def filter_by_date_range(self, from_date, to_date):
        """Filters the collection for only Entries from a date range, includes from & to dates"""
        to_date += datetime.timedelta(days=1)  # add 1 day so original to_date will be included in results
        while any(entry.date_created < from_date for entry in self.entries):
            for entry in self.entries:
                if entry.date_created < from_date:
                    self.entries.remove(entry)
        while any(entry.date_created >= to_date for entry in self.entries):
            for entry in self.entries:
                if entry.date_created >= to_date:
                    self.entries.remove(entry)
        return self.entries

    def filter_by_time_spent(self, minutes):
        """Filters the collection for only Entries that took a certain # of minutes"""
        while any(entry.time_spent != minutes for entry in self.entries):
            for entry in self.entries:
                if entry.time_spent != minutes:
                    self.entries.remove(entry)
        return self.entries

    def filter_by_regex_search(self, search_string):
        """Filters the collection for only Entries that contain a search string in Task Name or Notes"""
        title_matches = []
        while any(re.search(search_string, entry.task_name) for entry in self.entries):
            for entry in self.entries:
                if re.search(search_string, entry.task_name):
                    title_matches.append(entry)
                    self.entries.remove(entry)
        notes_matches = []
        while any(re.search(search_string, entry.notes) for entry in self.entries):
            for entry in self.entries:
                if re.search(search_string, entry.notes):
                    notes_matches.append(entry)
                    self.entries.remove(entry)
        self.entries = title_matches + notes_matches
        return self.entries
