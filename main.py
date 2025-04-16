import json
from library import Book, DigitalBook, PrintedBook, LibrarySystem
from user import User
from exceptions import BookAlreadyBorrowedError, BookNotFoundError, UserLimitExceededError, UserNotFoundError

def main():
    lms = LibrarySystem()
    lms.load_data()

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Register User")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Search Books")
        print("6. Show All Users")
        print("7. Show All Books")
        print("8. Check Overdue Books")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")
            book_type = input("Enter book type (digital/printed): ").lower()
            if book_type == "digital":
                file_size = float(input("Enter file size in MB: "))
                book = DigitalBook(title, author, isbn, file_size)
            elif book_type == "printed":
                page_count = int(input("Enter page count: "))
                book = PrintedBook(title, author, isbn, page_count)
            else:
                print("Invalid book type.")
                continue
            lms.add_book(book)
        elif choice == "2":
            user_id = int(input("Enter user ID: "))
            name = input("Enter user name: ")
            user = User(user_id, name)
            lms.add_user(user)

        elif choice == "3":
            user_id = int(input("Enter user ID: "))  
            isbn = input("Enter book ISBN: ")
            lms.borrow_book(user_id, isbn)  

        elif choice == "4":
            user_id = int(input("Enter user ID: "))
            isbn = input("Enter book ISBN: ")
            lms.return_book(user_id, isbn)

        elif choice == "5":
            title = input("Enter book title to search (leave empty if not searching by title): ")
            author = input("Enter book author to search (leave empty if not searching by author): ")
            available = input("Search for available books only? (yes/no): ").lower()
            available = True if available == 'yes' else False if available == 'no' else None
            results = lms.search_books(title=title, author=author, available=available)
            if results:
                print("Search results:")
                for book in results:
                    print(book)
            else:
                print("No books found.")

        elif choice == "6":
            print("\nAll Users:")
            for user in lms._users.values():
                print(user)

        elif choice == "7":
            print("\nAll Books:")
            for book in lms._books.values():
                print(book)

        elif choice == "8":
            user_id = int(input("Enter user ID to check overdue books: "))
            try:
                user = lms.find_user(user_id)
                overdue_books = user.get_overdue_books()
                if overdue_books:
                    print("Overdue books:")
                    for book, days_overdue in overdue_books:
                        print(f"{book} - {days_overdue} days overdue")
                else:
                    print("No overdue books.")
            except UserNotFoundError as e:
                print(e)

        elif choice == "9":
            lms.save_data()
            print("Exiting the Library Management System.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()