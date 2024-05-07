class BookRepository:
    def __init__(self):
        self.books = []

    def get_one(self, book_id):
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def create_one(self, book):
        self.books.append(book)

    def get_all(self):
        return self.books

    def get_books_by_library(self, library_id):
        return [book for book in self.books if book.library_id == library_id]
