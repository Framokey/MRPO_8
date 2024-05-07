from flask import Flask, render_template, request, redirect, url_for, json, Response
from models import *
from repository import *

app = Flask(__name__, template_folder='template')

# Инициализация репозиториев
book_repo = BookRepository()
author_repo = AuthorRepository()
library_repo = LibraryRepository()
reader_repo = ReaderRepository()

# Загрузка данных из файла
with open('./data/data.json', 'r', encoding='utf8') as f:
    data = json.load(f)

for book_data in data['books']:
    book = Book(**book_data)
    book_repo.create_one(book)

for author_data in data['authors']:
    author = Author(**author_data)
    author_repo.create_one(author)

for library_data in data['libraries']:
    library = Library(**library_data)
    library_repo.create_one(library)

for reader_data in data['readers']:
    reader = Reader(**reader_data)
    reader_repo.add_one(reader)

library_repo.libraries[0].add_book(book_repo.books[0])
library_repo.libraries[0].add_book(book_repo.books[1])
library_repo.libraries[1].add_book(book_repo.books[2])
library_repo.libraries[1].add_book(book_repo.books[3])

print(library_repo.get_books_from_library('Улица Библиотечная, 1'))
print(library_repo.get_all_addresses())

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print('im here')
        selected_library = request.form.get('library')
        print(selected_library)
        return redirect(url_for('books', library_address=selected_library))

    return render_template('index.html', libraries=library_repo.get_all_addresses())


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author_name = request.form['author_name']
        library_address = request.form['library_address']
        book = Book(title, author_name)
        author = author_repo.get_one_by_name(author_name)
        library = library_repo.get_one_by_address(library_address)
        book.author = author
        book.library = library
        book_repo.create_one(book)
        return redirect(url_for('home'))
    return render_template('add_book.html')


@app.route('/add_reader', methods=['GET', 'POST'])
def add_reader():
    if request.method == 'POST':
        ticket_id = request.form['ticket_id']
        name = request.form['name']
        r = Reader(ticket_id, name)
        reader_repo.add_one(r)
        return redirect(url_for('readers'))
    return render_template('add_reader.html')


@app.route('/readers')
def readers():
    return render_template('readers.html', readers=reader_repo.get_all())


@app.route('/books/<library_address>')
def books(library_address):
    print(library_address)
    books = library_repo.get_books_from_library(library_address)
    print(1, books)
    return render_template('books.html', books=books[0], library_address=library_address)

@app.route('/check_books', methods=['POST'])
def check_books():
    # Получаем данные из запроса
    data = request.json


    # for lib in library_repo.libraries:
    #     if lib.address == library_address:
    #         for book in lib.books:
    #             if book.title == book_title:
    #                 return Response("Книга найдена", status=200)
    # return Response("Книга не найдена", status=404)


if __name__ == '__main__':
    app.run(debug=True)
