import json
import os
from datetime import datetime

# File to store library data
LIBRARY_FILE = "library_data.json"

class LibraryManager:
    """A class to manage library operations"""
    
    def __init__(self):
        """Initialize the library manager and load existing data"""
        self.books = {}
        self.borrowed_records = []
        self.load_data()
    
    def load_data(self):
        """Load library data from file"""
        if os.path.exists(LIBRARY_FILE):
            try:
                with open(LIBRARY_FILE, 'r') as file:
                    data = json.load(file)
                    self.books = data.get('books', {})
                    self.borrowed_records = data.get('borrowed_records', [])
                print("✓ Library data loaded successfully!")
            except Exception as e:
                print(f"Error loading data: {e}")
                self.books = {}
                self.borrowed_records = []
        else:
            print("✓ New library initialized!")
    
    def save_data(self):
        """Save library data to file"""
        try:
            data = {
                'books': self.books,
                'borrowed_records': self.borrowed_records
            }
            with open(LIBRARY_FILE, 'w') as file:
                json.dump(data, file, indent=4)
            print("✓ Data saved successfully!")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def add_book(self, book_id, title, author, quantity):
        """
        Add a new book to the library
        
        Args:
            book_id (str): Unique identifier for the book
            title (str): Title of the book
            author (str): Author of the book
            quantity (int): Number of copies available
        """
        if book_id in self.books:
            print(f"✗ Book with ID '{book_id}' already exists!")
            return False
        
        self.books[book_id] = {
            'title': title,
            'author': author,
            'quantity': quantity,
            'available': quantity,
            'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_data()
        print(f"✓ Book '{title}' added successfully!")
        return True
    
    def view_all_books(self):
        """Display all books in the library"""
        if not self.books:
            print("\n✗ Library is empty!")
            return
        
        print("\n" + "="*80)
        print(f"{'ID':<10} {'Title':<30} {'Author':<20} {'Available':<8} {'Total':<8}")
        print("="*80)
        
        for book_id, book_info in self.books.items():
            print(f"{book_id:<10} {book_info['title']:<30} {book_info['author']:<20} "
                  f"{book_info['available']:<8} {book_info['quantity']:<8}")
        
        print("="*80 + "\n")
    
    def search_book(self, search_term):
        """
        Search for books by title or author
        
        Args:
            search_term (str): The search query
        """
        search_term = search_term.lower()
        results = {}
        
        for book_id, book_info in self.books.items():
            if (search_term in book_info['title'].lower() or 
                search_term in book_info['author'].lower()):
                results[book_id] = book_info
        
        if not results:
            print(f"\n✗ No books found matching '{search_term}'")
            return
        
        print(f"\n{'='*80}")
        print(f"Search Results for: '{search_term}'")
        print(f"{'='*80}")
        print(f"{'ID':<10} {'Title':<30} {'Author':<20} {'Available':<8} {'Total':<8}")
        print(f"{'-'*80}")
        
        for book_id, book_info in results.items():
            print(f"{book_id:<10} {book_info['title']:<30} {book_info['author']:<20} "
                  f"{book_info['available']:<8} {book_info['quantity']:<8}")
        
        print(f"{'='*80}\n")
    
    def borrow_book(self, book_id, member_name):
        """
        Borrow a book from the library
        
        Args:
            book_id (str): ID of the book to borrow
            member_name (str): Name of the member borrowing
        """
        if book_id not in self.books:
            print(f"✗ Book with ID '{book_id}' not found!")
            return False
        
        book = self.books[book_id]
        
        if book['available'] <= 0:
            print(f"✗ '{book['title']}' is currently not available!")
            return False
        
        # Update availability
        book['available'] -= 1
        
        # Record the borrowing
        borrow_record = {
            'book_id': book_id,
            'title': book['title'],
            'member_name': member_name,
            'borrow_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'borrowed'
        }
        self.borrowed_records.append(borrow_record)
        
        self.save_data()
        print(f"✓ '{book['title']}' borrowed successfully by {member_name}!")
        return True
    
    def return_book(self, book_id, member_name):
        """
        Return a borrowed book to the library
        
        Args:
            book_id (str): ID of the book to return
            member_name (str): Name of the member returning
        """
        if book_id not in self.books:
            print(f"✗ Book with ID '{book_id}' not found!")
            return False
        
        # Find the matching borrow record
        borrow_found = False
        for i, record in enumerate(self.borrowed_records):
            if (record['book_id'] == book_id and 
                record['member_name'] == member_name and 
                record['status'] == 'borrowed'):
                
                # Update the record
                self.borrowed_records[i]['status'] = 'returned'
                self.borrowed_records[i]['return_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                borrow_found = True
                break
        
        if not borrow_found:
            print(f"✗ No active borrow record found for {member_name} for book ID '{book_id}'!")
            return False
        
        # Update availability
        self.books[book_id]['available'] += 1
        
        self.save_data()
        print(f"✓ '{self.books[book_id]['title']}' returned successfully by {member_name}!")
        return True
    
    def view_borrow_history(self):
        """Display the borrow history"""
        if not self.borrowed_records:
            print("\n✗ No borrow history available!")
            return
        
        print("\n" + "="*100)
        print(f"{'Book ID':<10} {'Title':<30} {'Member':<20} {'Borrow Date':<20} {'Status':<10}")
        print("="*100)
        
        for record in self.borrowed_records:
            status = record['status']
            print(f"{record['book_id']:<10} {record['title']:<30} {record['member_name']:<20} "
                  f"{record['borrow_date']:<20} {status:<10}")
        
        print("="*100 + "\n")
    
    def get_book_status(self, book_id):
        """Display detailed status of a specific book"""
        if book_id not in self.books:
            print(f"✗ Book with ID '{book_id}' not found!")
            return
        
        book = self.books[book_id]
        print(f"\n{'='*50}")
        print(f"Book Details:")
        print(f"{'='*50}")
        print(f"ID: {book_id}")
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print(f"Total Copies: {book['quantity']}")
        print(f"Available: {book['available']}")
        print(f"Borrowed: {book['quantity'] - book['available']}")
        print(f"Date Added: {book['date_added']}")
        print(f"{'='*50}\n")


def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("         LIBRARY MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Add a new book")
    print("2. View all books")
    print("3. Search for a book")
    print("4. Borrow a book")
    print("5. Return a book")
    print("6. View borrow history")
    print("7. Get book status")
    print("8. Exit")
    print("="*50)


def main():
    """Main function to run the library management system"""
    library = LibraryManager()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == '1':
            # Add a new book
            print("\n--- Add New Book ---")
            book_id = input("Enter book ID: ").strip()
            title = input("Enter book title: ").strip()
            author = input("Enter author name: ").strip()
            try:
                quantity = int(input("Enter quantity: ").strip())
                if quantity <= 0:
                    print("✗ Quantity must be greater than 0!")
                    continue
                library.add_book(book_id, title, author, quantity)
            except ValueError:
                print("✗ Please enter a valid number for quantity!")
        
        elif choice == '2':
            # View all books
            print("\n--- All Books in Library ---")
            library.view_all_books()
        
        elif choice == '3':
            # Search for a book
            print("\n--- Search Books ---")
            search_term = input("Enter book title or author name: ").strip()
            if search_term:
                library.search_book(search_term)
            else:
                print("✗ Please enter a search term!")
        
        elif choice == '4':
            # Borrow a book
            print("\n--- Borrow a Book ---")
            book_id = input("Enter book ID: ").strip()
            member_name = input("Enter your name: ").strip()
            if book_id and member_name:
                library.borrow_book(book_id, member_name)
            else:
                print("✗ Please enter both book ID and member name!")
        
        elif choice == '5':
            # Return a book
            print("\n--- Return a Book ---")
            book_id = input("Enter book ID: ").strip()
            member_name = input("Enter your name: ").strip()
            if book_id and member_name:
                library.return_book(book_id, member_name)
            else:
                print("✗ Please enter both book ID and member name!")
        
        elif choice == '6':
            # View borrow history
            print("\n--- Borrow History ---")
            library.view_borrow_history()
        
        elif choice == '7':
            # Get book status
            print("\n--- Book Status ---")
            book_id = input("Enter book ID: ").strip()
            if book_id:
                library.get_book_status(book_id)
            else:
                print("✗ Please enter a book ID!")
        
        elif choice == '8':
            print("\n✓ Thank you for using Library Management System! Goodbye!")
            break
        
        else:
            print("✗ Invalid choice! Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()