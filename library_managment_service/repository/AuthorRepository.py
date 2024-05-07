class AuthorRepository:
    def __init__(self):
        self.authors = {}

    def get_all(self):
        return list(self.authors.values())

    def create_one(self, author, book=None):
        if book and author not in self.authors:
            self.authors[author.id] = author
            if book:
                book.author = author