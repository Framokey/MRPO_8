from flask import Flask, render_template, request, redirect, url_for, json, Response, jsonify
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_library = request.form.get('library_address')
        return redirect(url_for('books', library_address=selected_library))
    return render_template('index.html', libraries=library_repo.get_all_addresses())


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book_title = request.form['book_title']
        library_address = request.form['library_address']
        year_published = request.form['year_published']
        book = Book(len(book_repo.books), book_title, 'Петр Петров', year_published)
        book_repo.create_one(book)
        library = library_repo.get_library_by_address(library_address)
        library.add_book(book)

        return redirect(url_for('index'))
    return render_template('add_book.html', libraries=library_repo.get_all_addresses())


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
    books = library_repo.get_books_from_library(library_address)
    return render_template('books.html', books=books[0], library_address=library_address)


@app.route('/check_books', methods=['POST'])
def check_books():
    # Получаем данные из запроса
    data = request.json

    # Инициализация списка результатов
    results = {}

    # Проходим по каждому адресу библиотеки из запроса
    for address, books in data.items():
        # Находим книги по названиям в репозитории
        found_books = library_repo.find_books_by_titles([book['name'] for book in books])

        # Обновляем статусы книг
        status_updates = {book['name']: "В наличии" if book['name'] in found_books else "Нет в наличии" for book in books}

        # Сохраняем обновленные статусы в исходный формат
        updated_books = [{"name": name, "status": status} for name, status in status_updates.items()]

        # Добавляем обновленные книги в результаты
        results[address] = updated_books

    # Возвращаем результаты
    return jsonify(results)


@app.route('/libraries', methods=['GET'])
def libraries():
    return json.dumps({"libraries": [{"address": a.address} for a in library_repo.get_all()]}, indent=4)


if __name__ == '__main__':
    app.run(debug=True)
