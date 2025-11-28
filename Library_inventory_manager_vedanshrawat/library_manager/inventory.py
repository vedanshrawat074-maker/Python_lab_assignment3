# library_manager/inventory.py
import json
import logging
from pathlib import Path

from .book import Book

logger = logging.getLogger(__name__)


class LibraryInventory:
    # Manages list of Book objects and JSON file

    def __init__(self, storage_path=None):
        """Initialize inventory and load any existing catalog file.

        If storage_path is not provided, default to a file named
        `catalog.json` located at the project root (two folders up from
        this module).
        """
        if storage_path is None:
            storage_path = Path(__file__).resolve().parent.parent / "catalog.json"
        self.storage_path = Path(storage_path)
        self.books = []
        self.load_from_file()

    # ---------- File handling ----------

    def load_from_file(self):
        #Load books from JSON. Handle missing / bad file#
        if not self.storage_path.exists():
            logger.info("No catalog file found. Starting with empty list.")
            self.books = []
            return

        try:
            text = self.storage_path.read_text(encoding="utf-8")
            raw_list = json.loads(text)
            self.books = [Book.from_dict(item) for item in raw_list]
            logger.info("Loaded %d books from file.", len(self.books))
        except json.JSONDecodeError as e:
            logger.error("Catalog file is corrupted: %s", e)
            self.books = []
        except OSError as e:
            logger.error("Error reading catalog file: %s", e)
            self.books = []

    def save_to_file(self):
        #Save all books to JSON file
        try:
            data = [book.to_dict() for book in self.books]
            self.storage_path.write_text(
                json.dumps(data, indent=2),
                encoding="utf-8",
            )
            logger.info("Saved %d books to file.", len(self.books))
        except OSError as e:
            logger.error("Error saving catalog file: %s", e)

    # ---------- Inventory working ----------

    def add_book(self, book):
        # Add a book to the inventory and persist it. Return True on success.
        self.books.append(book)
        logger.info("Added book: %s", book)
        self.save_to_file()
        return True

    def search_by_title(self, title_query):
        #Return list of books where title contains query (case-insensitive)
        title_query = title_query.lower()
        result = []
        for b in self.books:
            if title_query in b.title.lower():
                result.append(b)
        return result

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        #Return list of all books
        return self.books[:]
    
    # ---------- Book lifecycle methods ----------
    def issue_book(self, isbn):
        """Marks a book as issued if it is available; returns True on success."""
        book = self.search_by_isbn(isbn)
        if book and book.issue():
            self.save_to_file()
            logger.info("Issued book: %s", book)
            return True
        return False

    def return_book(self, isbn):
        """Marks a book as returned if it's currently issued; returns True on success."""
        book = self.search_by_isbn(isbn)
        if book and book.return_book():
            self.save_to_file()
            logger.info("Returned book: %s", book)
            return True
        return False
    
    