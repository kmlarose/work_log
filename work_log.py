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
    entry.save_new_entry()
    return entry


def display_entries(collection):
    """Entries are displayed one at a time with the ability to edit, delete, or page through records"""
    if len(collection) == 0:
        print('sorry, no results found.')
        return input('press enter to continue...')

    # display entries one at a time
    user_choice = ''
    page = 1
    while user_choice.upper() != 'B':
        clear_console()
        print('Result {} of {}'.format(page, len(collection)))
        print('='*15)
        print(collection.entries[page-1], end='\n\n')

        # determine if user is looking at first and/or last page
        on_first_page = page == 1
        on_last_page = page == len(collection)

        # print the pagination nav menu
        print('Options:')
        print('[E] Edit [D] Delete')
        # nav options
        if not on_first_page:
            print('[P] Previous', end=' ')
        if not on_last_page:
            print('[N] Next', end=' ')
        print('[B] Back to Lookup Menu')

        user_choice = input('> ')
        if user_choice.upper() == 'E':
            # TODO-kml: Entries can be edited, letting user change the date, task name, time spent, and/or notes.
            while user_choice.upper() != 'B':
                clear_console()
                print(collection.entries[page - 1])
                print('What would you like to edit?')
                print('[D] Date [T] Task Name [S] Time Spent [N] Notes [B] Back')
                user_choice = input('> ')
                if user_choice.upper() == 'D':
                    print('Current Date: {}'.format(collection.entries[page-1].date))
                    # get a valid date
                    while True:
                        new_date = input('new date (MM-DD-YYYY): ')
                        try:
                            new_date = datetime.datetime.strptime(new_date, '%m-%d-%Y')
                        except ValueError:
                            print('Please enter a valid date in MM-DD-YYYY format')
                        else:
                            break
                    # confirm user is sure...
                    print('Change Entry Date from {} to {}.'.format(collection.entries[page-1].date, new_date.strftime('%m-%d-%Y')))
                    are_you_sure = input('Are you sure? [y/N]?: ')
                    if are_you_sure.upper() == 'Y':
                        collection.entries[page - 1].date_created = new_date
                        collection.entries[page - 1].save()
                        print('Changes Saved!')
                if user_choice.upper() == 'T':
                    print('Current Task Name: {}'.format(collection.entries[page -1].task_name))
                    new_name = input('new name: ')
                    print('Change Entry Task Name from {} to {}'.format(collection.entries[page-1].task_name, new_name))
                    are_you_sure = input('Are you sure? [y/N]?: ')
                    if are_you_sure.upper() == 'Y':
                        collection.entries[page - 1].task_name = new_name
                        collection.entries[page - 1].save()
                        print('Changes Saved!')
                if user_choice.upper() == 'S':
                    print('Current Time Spent: {}'.format(collection.entries[page - 1].time_spent))
                    while True:
                        new_time = input('new time spent (minutes): ')
                        try:
                            new_time = int(new_time)
                        except ValueError:
                            print('Please enter an integer...')
                        else:
                            if new_time < 1:
                                print('Please enter a valid # of minutes...')
                            else:
                                break
                    print('Change Entry Time Spent from {} to {}'.format(collection.entries[page - 1].time_spent,
                                                                         new_time))
                    are_you_sure = input('Are you sure? [y/N]?: ')
                    if are_you_sure.upper() == 'Y':
                        collection.entries[page - 1].time_spent = new_time
                        collection.entries[page - 1].save()
                        print('Changes Saved!')
                if user_choice.upper() == 'N':
                    print('Current Notes: {}'.format(collection.entries[page - 1].notes))
                    new_notes = input('new notes: ')
                    print(
                        'Change Entry Notes from {} to {}'.format(collection.entries[page - 1].notes, new_notes))
                    are_you_sure = input('Are you sure? [y/N]?: ')
                    if are_you_sure.upper() == 'Y':
                        collection.entries[page - 1].notes = new_notes
                        collection.entries[page - 1].save()
                        print('Changes Saved!')
        if user_choice.upper() == 'D':
            are_you_sure = input('Are you sure you want to delete this entry? [y/N]: ')
            if are_you_sure.upper() == 'Y':
                collection.entries[page-1].delete_from_data_file()
                del collection.entries[page-1]
                if on_first_page and on_last_page:
                    return user_choice.upper()  # Exit the Results Menu
                elif on_last_page:
                    page -= 1
        if user_choice.upper() == 'P' and not on_first_page:
            page -= 1
        if user_choice.upper() == 'N' and not on_last_page:
            page += 1
    return user_choice.upper()  # Exit the Results Menu


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
                    search_string = input('Please enter text to search for: ')
                    collection.filter_by_exact_search(search_string)
                    display_entries(collection)
                if menu_choice.upper() == 'P':  # find by pattern
                    regex_pattern = input('Please enter regex pattern to search for: ')
                    collection.filter_by_pattern_search(regex_pattern)
                    display_entries(collection)


# TODO-kml: Entries can be searched for and found based on a date range. For example between 01/01/2016 and 12/31/2016.

if __name__ == '__main__':
    run_console_ui()
