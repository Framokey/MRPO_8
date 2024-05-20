from flask import Flask, render_template, request, jsonify, Request, Response
import json
import requests

app = Flask(__name__, template_folder='template')

# Простое хранилище данных для отслеживаемых книг
tracked_books = {}


def load_tracked_books():
    global tracked_books
    try:
        with open('tracked_books.json', 'r') as file:
            tracked_books = json.load(file)
    except FileNotFoundError:
        tracked_books = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    global tracked_books
    load_tracked_books()  # Загружаем отслеживаемые книги при каждом запросе

    if request.method == 'POST':
        library_address = request.form['library_address']
        book_title = request.form['book_title']

        # Проверяем, есть ли уже отслеживаемые книги для этой библиотеки
        if library_address not in tracked_books:
            tracked_books[library_address] = []

        # Добавляем книгу в список отслеживаемых для этой библиотеки
        tracked_books[library_address].append(book_title)

        # Сохраняем изменения в файле
        with open('tracked_books.json', 'w') as file:
            json.dump(tracked_books, file, indent=4)  # Используем indent для лучшей читаемости

        return "Книга добавлена в отслеживание."

    # Отображаем форму для выбора библиотеки и книги
    return render_template('index.html')


@app.route('/tracked_books')
def tracked_books_page():
    check_books()
    # Загружаем отслеживаемые книги из файла
    with open('tracked_books.json', 'r') as file:
        tracked_books_data = json.load(file)

    return render_template('tracked_books.html', tracked_books=tracked_books_data)


def check_books():
    with open('tracked_books.json', 'r') as file:
        tracked_books_data = json.load(file)

    response = requests.post('http://localhost:5000/check_books', json=tracked_books_data)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
