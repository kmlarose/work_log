import datetime
import json

from entry import Entry


class EntryCollection:
    """A collection of all the log Entries from the data file"""

    def __init__(self):
        self.entries = []
        # import all of the JSON strings as dictionaries
        saved_data = []
        with open('work_log_entries.txt', 'r') as entries_log:
            [saved_data.append(json.loads(line[:-1])) for line in entries_log]  # slice excludes the '\n'
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
        to_date += datetime.timedelta(days=1)
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

    # TODO-kml: enter a string and be presented with entries containing that string in the name or notes
    def filter_by_exact_search(self, search_string):
        """Filters the collection for only Entries that match a search string"""
        pass

    # TODO-kml: enter a regex and be presented with entries matching that pattern in the name or notes
    def filter_by_pattern_search(self, regex_pattern):
        """Filters the collection for only Entries that match a regex pattern"""
        pass
