class BookNotFoundError(Exception):
    pass
class BookAlreadyBorrowedError(Exception):
    pass
class UserLimitExceededError(Exception):
    pass
class UserNotFoundError(Exception):
    pass