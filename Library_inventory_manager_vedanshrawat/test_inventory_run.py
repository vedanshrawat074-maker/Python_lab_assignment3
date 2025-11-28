import library_manager.book as book_mod
from library_manager.inventory import LibraryInventory
from library_manager.book import Book
import inspect
import importlib

importlib.reload(book_mod)
print('book module file:', book_mod.__file__)
print('Book init signature:', inspect.signature(Book.__init__))
inv = LibraryInventory()
print('Before count:', len(inv.display_all()))
inv.add_book(Book('Test Title', 'Author', 'ISBN-0001'))
print('After count:', len(inv.display_all()))
print('Book object:', inv.search_by_isbn('ISBN-0001'))
inv.issue_book('ISBN-0001')
print('After issue:', inv.search_by_isbn('ISBN-0001'))
inv.return_book('ISBN-0001')
print('After return:', inv.search_by_isbn('ISBN-0001'))
