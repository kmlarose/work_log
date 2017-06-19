import json

from entry import Entry


class EntryCollection:
    """A collection of all the log Entries from the data file"""
    def __init__(self):
        self.entries = []
        saved_data = []
        # import all of the JSON strings as dictionaries
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
