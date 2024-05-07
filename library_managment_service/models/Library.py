class Library:
    def __init__(self, address):
        self.address = address
        self.books = []  # Список книг в библиотеке
        self.readers = []  # Список читателей

    def add_book(self, book):
        self.books.append(book)

    def add_reader(self, reader):
        self.readers.append(reader)

    def find_book_by_title(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None

    def find_reader_by_ticket_id(self, ticket_id):
        for reader in self.readers:
            if reader.ticket_id == ticket_id:
                return reader
        return None
