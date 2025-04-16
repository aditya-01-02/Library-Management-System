from datetime import datetime, timedelta
from exceptions import BookAlreadyBorrowedError

class User:
    BORROW_PERIOD = timedelta(days=14)  

    def __init__(self, user_id, name):
        self._user_id = user_id
        self._name = name
        self._borrowed_books = []

    def borrow_book(self, book):
        try:
            if book.borrow():
                self._borrowed_books.append((book, datetime.now()))
                print(f"{self._name} borrowed {book}")
        except BookAlreadyBorrowedError as e:
            print(e)

    def return_book(self, book):
        for borrowed_book, borrow_date in self._borrowed_books:
            if borrowed_book == book:
                self._borrowed_books.remove((borrowed_book, borrow_date))
                borrowed_book.return_book()
                overdue_days = (datetime.now() - borrow_date).days - self.BORROW_PERIOD.days
                if overdue_days > 0:
                    print(f"{self._name} returned {book} with {overdue_days} days overdue. Penalty applies.")
                else:
                    print(f"{self._name} returned {book} on time.")
                return
        print(f"{self._name} does not have {book}")

    def get_overdue_books(self):
        overdue_books = []
        for book, borrow_date in self._borrowed_books:
            if datetime.now() > borrow_date + self.BORROW_PERIOD:
                overdue_books.append((book, (datetime.now() - borrow_date).days - self.BORROW_PERIOD.days))
        return overdue_books

    def __str__(self):
        return f"User {self._user_id}: {self._name}"
