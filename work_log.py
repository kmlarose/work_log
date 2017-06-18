import os

from entry import Entry


def clear_console():
    """clears the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def add_new_entry():
    """Collects user input for the New Log Entry"""
    clear_console()
    print('Add New Entry')
    entry_name = input('Entry Name: ')
    entry_time = input('How many minutes did it take?: ')
    # TODO-kml: transform the entry_time into a timedelta object
    entry_note = input('Any additional notes?: ')
    return Entry(entry_name, entry_time, entry_note)


MAIN_MENU = ('[A] Add New Entry\n'
             '[L] Lookup Previous Entries\n'
             '[Q] Quit')


menu_choice = ''
while menu_choice.upper() != 'Q':
    clear_console()
    print('    Work Log')
    print(MAIN_MENU)

    menu_choice = input('> ')
    if menu_choice.upper() == 'A':
        new_entry = add_new_entry()
        print('Added new entry: {}'.format(new_entry))
        input('Press enter to continue...')
    if menu_choice.upper() == 'L':
        print('Lookup Previous Entries')
        print('Under Construction')
        input('Press enter to continue...')

# As a user of the script, if I choose to find a previous entry,
# I should be presented with four options:
#       find by date
#       find by time spent
#       find by exact search
#       find by pattern
# Note:
# When finding by date, I should be presented with a list of dates with entries
# and be able to choose one to see entries from.
# When finding by time spent, I should be allowed to enter the number of minutes a task took
# and be able to choose one to see entries from.
# When finding by an exact string, I should be allowed to enter a string
# and then be presented with entries containing that string in the task name or notes.
# When finding by a pattern, I should be allowed to enter a regular expression
# and then be presented with entries matching that pattern in their task name or notes.

# When displaying the entries, the entries should be displayed in a readable format with
# the date, task name, time spent, and notes information.

# EXTRA CREDIT
# ============
# Entries can be deleted and edited, letting user change the date,
# task name, time spent, and/or notes.
# Entries can be searched for and found based on a date range.
# For example between 01/01/2016 and 12/31/2016.
# Entries are displayed one at a time with the ability to page through records
# (previous/next/back).

# NOTE:
# To get an "Exceeds Expectations" grade for this project,
# you'll need to complete each of the items in this section.
# See the rubric in the "How You'll Be Graded" tab above for details on how you'll be graded.
# If you’re shooting for the "Exceeds Expectations" grade,
# it is recommended that you mention so in your submission notes.
# Passing grades are final. If you try for the "Exceeds Expectations" grade,
# but miss an item and receive a “Meets Expectations” grade, you won’t get a second chance.
# Exceptions can be made for items that have been misgraded in review.

# Make sure your script runs without errors.
# Catch exceptions and report errors to the user in a meaningful way.
