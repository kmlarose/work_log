import datetime
import os

from entry import Entry
from entry_collections import EntryCollection


def clear_console():
    """clears the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def add_new_entry():
    """Collects user input for the New Log Entry"""
    clear_console()
    print('Add New Entry')
    entry_name = input('Entry Name: ')
    while True:  # continue prompting until a positive integer is given
        entry_time = input('How many minutes did it take?: ')
        try:
            entry_time = int(entry_time)
        except ValueError:
            print('Please enter an integer: ')
        else:
            if entry_time <= 0:
                print('Please enter a valid # of minutes...')
            else:
                break
    entry_note = input('Any additional notes?: ')
    entry = Entry(entry_name, entry_time, entry_note)
    entry.save()
    return entry


def display_entries(collection):
    if len(collection) == 1:
        plural = ''
    else:
        plural = 's'
    print('{} result{}:'.format(len(collection), plural))
    [print(entry, end='\n\n') for entry in collection.entries]
    return input('press enter to continue...')


def run_console_ui():
    """Prints menus & prompts to the console and collects user input"""
    main_menu = ('[A] Add New Entry\n'
                 '[L] Lookup Previous Entries\n'
                 '[Q] Quit')

    lookup_menu = ('[D] Find by Date\n'
                   '[T] Find by Time Spent\n'
                   '[E] Find by Exact Search\n'
                   '[P] Find by Pattern\n'
                   '[B] Back to Main Menu')

    # Main Menu Loop
    menu_choice = ''
    while menu_choice.upper() != 'Q':
        # display main menu
        clear_console()
        print('    Work Log')
        print(main_menu)

        # handle the user's choice
        menu_choice = input('> ')
        if menu_choice.upper() == 'A':
            new_entry = add_new_entry()
            print('Added new entry!')
            print(new_entry)
        if menu_choice.upper() == 'L':

            # Lookup Menu Loop
            while menu_choice.upper() != 'B':
                # load entries
                collection = EntryCollection()

                # display lookup menu
                clear_console()
                print('    Work Log')
                print('Lookup Previous Entries')
                print(lookup_menu)

                # handle the user's choice
                menu_choice = input('> ')
                if menu_choice.upper() == 'D':  # find by date
                    clear_console()
                    dates = set()
                    [dates.add(entry.date) for entry in collection]
                    dates = list(dates)
                    dates.sort()
                    while True:
                        print('    Work Log')
                        print('Choose a date to see entries from')
                        [print(date) for date in dates]
                        chosen_date = input('(MM-DD-YYYY) format > ')
                        try:
                            chosen_date = datetime.datetime.strptime(chosen_date, '%m-%d-%Y')
                        except ValueError:
                            clear_console()
                            print('Please enter a date in the valid format')
                        else:
                            if chosen_date.strftime('%m-%d-%Y') not in dates:
                                clear_console()
                                print('hey-o! there are no entries with that date. Try another...')
                            else:
                                break
                    collection.filter_by_date(chosen_date)
                    display_entries(collection)
                if menu_choice.upper() == 'T':  # find by time spent
                    # TODO-kml: enter the number of minutes a task took and be able to choose one to see entries from
                    # get an int from the user
                    while True:
                        minutes = input('Please enter the # of minutes the task took: ')
                        try:
                            minutes = int(minutes)
                        except ValueError:
                            print('Please enter an integer...')
                        else:
                            if minutes <= 0:
                                print('Please enter a valid # of minutes...')
                            else:
                                break
                    collection.filter_by_time_spent(minutes)
                    display_entries(collection)
                if menu_choice.upper() == 'E':  # find by exact search
                    # TODO-kml: enter a string and be presented with entries containing that string in the name or notes
                    pass
                if menu_choice.upper() == 'P':  # find by pattern
                    # TODO-kml: enter a regex and be presented with entries matching that pattern in the name or notes
                    pass

# REQUIREMENTS:
# When displaying the entries, the entries should be displayed in a readable format with
# the date, task name, time spent, and notes information.

# Entries can be deleted and edited, letting user change the date, task name, time spent, and/or notes.
# Entries can be searched for and found based on a date range. For example between 01/01/2016 and 12/31/2016.
# Entries are displayed one at a time with the ability to page through records (previous/next/back).

if __name__ == '__main__':
    run_console_ui()
