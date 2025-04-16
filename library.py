from exceptions import BookAlreadyBorrowedError, BookNotFoundError, UserLimitExceededError, UserNotFoundError
import json
import datetime
from user import User


class Book:
    def __init__(self, title, author, isbn, available=True):
        self._title = title
        self._author = author
        self._isbn = isbn
        self._available = available

    def check_availability(self):
        return self._available

    def borrow(self):
        if self._available:
            self._available = False
            return True
        return False  

    def return_book(self):
        self._available = True

    def __str__(self):
        return f"{self._title} by {self._author} (ISBN: {self._isbn}) - {'Available' if self._available else 'Not Available'}"

class DigitalBook(Book):
    def __init__(self, title, author, isbn, file_size, available=True):
        super().__init__(title, author, isbn, available)
        self._file_size = file_size

    def __str__(self):
        return f"{super().__str__()} - File Size: {self._file_size}MB"

class PrintedBook(Book):
    def __init__(self, title, author, isbn, page_count, available=True):
        super().__init__(title, author, isbn, available)
        self._page_count = page_count

    def __str__(self):
        return f"{super().__str__()} - Pages: {self._page_count}"


class LibrarySystem:
    MAX_BORROW_LIMIT = 3  

    def __init__(self):
        self._books = {}
        self._users = {}

    def add_book(self, book):
        if book._isbn not in self._books:
            self._books[book._isbn] = book
            print(f"Added {book}")
        else:
            print(f"Book with ISBN {book._isbn} already exists.")

    def add_user(self, user):
        for existing_user in self._users.values():
            if existing_user._user_id == user._user_id:
                print(f"User with ID {user._user_id} already exists.")
                return
        self._users[user._user_id] = user
        print(f"Added {user}")

    def find_book(self, isbn):
        if isbn not in self._books:
            raise BookNotFoundError(f"Book with ISBN {isbn} not found.")
        return self._books[isbn]

    def find_user(self, user_id):
        normalized_user_id = str(user_id).strip().lower()  # Convert user_id to string and normalize
        for existing_user in self._users.values():
            if str(existing_user._user_id).lower() == normalized_user_id:  # Ensure existing_user._user_id is converted to string
                return existing_user
        raise UserNotFoundError(f"User with ID '{user_id}' not found.")
    
    def borrow_book(self, user_id, isbn):
        try:
            user = self.find_user(user_id)
            book = self.find_book(isbn)
            if len(user._borrowed_books) >= self.MAX_BORROW_LIMIT:
                raise UserLimitExceededError(f"User {user._name} has exceeded the borrow limit.")
            if book.borrow():
                user.borrow_book(book)
                print(f"Book '{book._title}' successfully borrowed by {user._name}.")
            else:
                print(f"The book '{book._title}' is already borrowed.")
        except (BookNotFoundError, UserNotFoundError, UserLimitExceededError) as e:
            print(e)
        finally:
            print("Borrow book operation completed.")

    def return_book(self, user_id, isbn):
        try:
            user = self.find_user(user_id)
            book = self.find_book(isbn)
            if not book.check_availability():
                book.return_book()
                user.return_book(book)
                print(f"Book '{book._title}' successfully returned by {user._name}.")
            else:
                print(f"The book '{book._title}' is already available.")
        except (BookNotFoundError, UserNotFoundError) as e:
            print(e)
        finally:
            print("Return book operation completed.")

    def search_books(self, title=None, author=None, available=None):
        results = []
        for book in self._books.values():
            if (title and title.lower() not in book._title.lower()) or \
               (author and author.lower() not in book._author.lower()) or \
               (available is not None and book.check_availability() != available):
                continue
            results.append(book)
        return results

    def save_data(self, book_file='books.json', user_file='users.json'):
        books_data = {isbn: vars(book) for isbn, book in self._books.items()}
        users_data = {user_id: {'user_id': user._user_id, 'name': user._name, 'borrowed_books': [(vars(book), date.isoformat()) for book, date in user._borrowed_books]} for user_id, user in self._users.items()}

        with open(book_file, 'w') as bf:
            json.dump(books_data, bf)

        with open(user_file, 'w') as uf:
            json.dump(users_data, uf)

    def load_data(self, book_file='books.json', user_file='users.json'):
        try:
            with open(book_file, 'r') as bf:
                books_data = json.load(bf)
                for isbn, book_data in books_data.items():
                    if 'file_size' in book_data:
                        book = DigitalBook(book_data['_title'], book_data['_author'], book_data['_isbn'], book_data['_file_size'], book_data['_available'])
                    elif 'page_count' in book_data:
                        book = PrintedBook(book_data['_title'], book_data['_author'], book_data['_isbn'], book_data['_page_count'], book_data['_available'])
                    else:
                        book = Book(book_data['_title'], book_data['_author'], book_data['_isbn'], book_data['_available'])
                    self._books[isbn] = book

            with open(user_file, 'r') as uf:
                users_data = json.load(uf)
                for user_id, user_data in users_data.items():
                    user = User(user_data['user_id'], user_data['name'])
                    for book_data, date_str in user_data['borrowed_books']:
                        book = self.find_book(book_data['_isbn'])
                        user._borrowed_books.append((book, datetime.fromisoformat(date_str)))
                    self._users[user_id] = user
        except FileNotFoundError:
            print("Data files not found. Starting with an empty library.")
