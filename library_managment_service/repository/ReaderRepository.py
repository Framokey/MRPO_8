class ReaderRepository:
    def __init__(self):
        self.readers = []

    def add_one(self, reader):
        self.readers.append(reader)

    def get_all(self):
        return self.readers
