class LibraryRepository:
    def __init__(self):
        self.libraries = []

    def get_all_addresses(self):
        return [library.address for library in self.libraries]

    def create_one(self, library):
        self.libraries.append(library)

    def get_books_from_library(self, address):
        return [library.books for library in self.libraries if library.address == address]

    def get_library_by_address(self, address):
        for library in self.libraries:
            if library.address == address:
                return library

    def get_all(self):
        return self.libraries

    def find_books_by_titles(self, titles):
        found_books = []
        for library in self.libraries:
            for book in library.books:
                if book.title in titles:
                    found_books.append(book.title)
        return found_books
