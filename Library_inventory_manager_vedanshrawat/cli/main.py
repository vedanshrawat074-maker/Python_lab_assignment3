import sys
from pathlib import Path
# This code navigates up two levels from cli/main.py to find the project root.
try:
    # Gets the current file's location, resolves it, and navigates up two parent directories
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    sys.path.append(str(PROJECT_ROOT))
except NameError:
    # Handles cases where _file_ might not be defined (less common)
    pass
# cli/main.py
from library_manager.book import Book
from library_manager.inventory import LibraryInventory, logger 
# --- Helper Functions ---
def get_input(prompt: str) -> str:
    """Gets validated, non-empty user input."""
    while True:
        try:
            user_input = input(prompt).strip()
            if user_input: return user_input
            print("Input required.")
        except KeyboardInterrupt: raise 

def main_menu():
    """Prints the required menu options (Task 4)."""
    print("\n" + "="*30)
    print("📚 LIBRARY MANAGER")
    print("1: Add Book | 2: Issue | 3: Return | 4: View All | 5: Search | 6: Exit")
    print("="*30)

# --- Handler Functions (Kept separate for cleaner main loop) ---
def add_book_handler(inventory):
    print("\n--- Add Book ---")
    title = get_input("Title: ")
    author = get_input("Author: ")
    isbn = get_input("ISBN: ")
    if inventory.add_book(Book(title, author, isbn,status="available")):
        print(f"✅ Added: {title}")

def search_handler(inventory):
    search_type = get_input("\nSearch by (1) Title or (2) ISBN? ")
    if search_type == '1':
        query = get_input("Enter Title (partial): ")
        results = inventory.search_by_title(query)
        print(f"\n--- {len(results)} Title Results ---")
        for book in results: print(str(book))
    elif search_type == '2':
        query = get_input("Enter ISBN (exact): ")
        result = inventory.search_by_isbn(query)
        print(str(result) if result else "Book not found.")
    else:
        print("Invalid search option.")

def view_all_handler(inventory):
    print("\n--- All Books ---")
    books = inventory.display_all()
    if not books:
        print("No books found.")
    else:
        for b in books:
            print(str(b))

def issue_handler(inventory):
    isbn = get_input("\nEnter ISBN to issue: ")
    if inventory.issue_book(isbn):
        print("✅ Book issued.")
    else:
        print("❌ Could not issue book. Check ISBN or availability.")

def return_handler(inventory):
    isbn = get_input("\nEnter ISBN to return: ")
    if inventory.return_book(isbn):
        print("✅ Book returned.")
    else:
        print("❌ Could not return book. Check ISBN or status.")

def run_cli():
    inventory = LibraryInventory()
    # Map menu choices to functions
    choices = {
        '1': add_book_handler,
        '2': issue_handler,
        '3': return_handler,
        '4': view_all_handler,
        '5': search_handler,
    }
    
    try:
        while True:
            main_menu()
            choice = get_input("Choice (1-6): ")

            if choice == '6':
                print("\n👋 Exiting.")
                logger.info("Application closed.")
                break
            
            handler = choices.get(choice)
            if handler:
                handler(inventory)
            else:
                print("❗ Invalid choice.")
                
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted.")
        logger.info("Application interrupted by user.")
    except Exception as e:
        logger.error(f"Critical error: {e}", exc_info=True)
        print("\n\n❌ A critical error occurred. Check logs.")

if __name__== '__main__':
    run_cli()
