# Library-Management-System

A command-line based Library Management System (LMS) built with Python, supporting book borrowing/returning, user registration, book search, and overdue tracking. It handles both digital and printed books with persistent data storage using JSON files.

    🚀 Features
    
    📖 Book Management: Add digital or printed books with ISBNs.
    
    👤 User Management: Register users with a unique user ID and name.
    
    🔄 Borrow/Return System: Users can borrow up to 3 books and return them.
    
    🔍 Search Books: Search by title, author, and availability.
    
    ⏳ Overdue Tracking: Detect overdue books and apply penalties.
    
    💾 Persistent Data: Save and load book/user data from JSON files.
    
    🚫 Custom Exception Handling: Clear error feedback for missing books, users, and limit violations.




🗂 File Structure

  📦Library-Management-System
  
    ├── main.py              # Command-line interface
    
    ├── library.py           # Core library logic (Books, LibrarySystem)
    
    ├── user.py              # User class and overdue logic
    
    ├── exceptions.py        # Custom exceptions
    
    ├── books.json           # Saved book data (auto-generated)
    
    ├── users.json           # Saved user data (auto-generated)
    
    └── README.md            # Project documentation



🛠 How to Run

Clone the repository:

    git clone https://github.com/your-username/Library-Management-System.git
    cd Library-Management-System

Run the program:

    python main.py

📋 Menu Options
1. Add Book
2. Register User
3. Borrow Book
4. Return Book
5. Search Books
6. Show All Users
7. Show All Books
8. Check Overdue Books
9. Exit



📌 Dependencies

No external packages required. Built with Python 3.x using only standard libraries.



💡 Custom Exceptions

BookNotFoundError

BookAlreadyBorrowedError

UserLimitExceededError

UserNotFoundError

Defined in exceptions.py to improve code readability and control flow.
