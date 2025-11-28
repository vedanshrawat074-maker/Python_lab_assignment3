class Book:

    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        # Ensure status is stored in lowercase for reliable comparison
        self.status = status.lower()

    def __str__(self):
        return (
            f"Title: {self.title} | Author: {self.author} | "
            f"ISBN: {self.isbn} | Status: {self.status.upper()}"
        )

    def to_dict(self):
        """Returns a dictionary for JSON serialization."""
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status,
        }

    def is_available(self):
        return self.status == "available"

    @classmethod
    def from_dict(cls, data: dict):
        """Create a Book instance from a dictionary returned by `to_dict`."""
        return cls(
            data.get("title"),
            data.get("author"),
            data.get("isbn"),
            data.get("status", "available"),
        )

    def issue(self):
        if self.is_available():
            self.status = "issued"
            return True  # Use booleans to indicate success/failure
        return False

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False
                   