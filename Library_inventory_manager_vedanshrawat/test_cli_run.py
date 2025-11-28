from library_manager.inventory import LibraryInventory
from library_manager.book import Book

# Import handlers from the CLI module
from cli.main import view_all_handler

inv = LibraryInventory()
inv.add_book(Book('CLI Test', 'Tester', 'CLI-ISBN-001'))
view_all_handler(inv)

# Issue and return tests
print('\nAttempting to issue a sample ISBN:')
print('issue result:', inv.issue_book('CLI-ISBN-001'))
print('\nAttempting to return a sample ISBN:')
print('return result:', inv.return_book('CLI-ISBN-001'))
