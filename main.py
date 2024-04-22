from flask import Flask, jsonify, request, json, session
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

# Create a Flask Instance
app = Flask(__name__)
api = Api(app)
db = SQLAlchemy()

# Configuration for SQLite database with file name (case.db)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Case.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# initalize the databse on the app
db.init_app(app)


# Create table...
class bookModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {"name": self.name, "author": self.author, "id": self.id}


# Create tables if not exists
with app.app_context():
    db.create_all()

famous_books = [
    {"book_id": 1, "name": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"book_id": 2, "name": "1984", "author": "George Orwell"},
    {"book_id": 3, "name": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"book_id": 4, "name": "Pride and Prejudice", "author": "Jane Austen"},
    {"book_id": 5, "name": "The Catcher in the Rye", "author": "J.D. Salinger"},
    {"book_id": 6, "name": "The Lord of the Rings", "author": "J.R.R. Tolkien"},
    {"book_id": 7, "name": "The Hobbit", "author": "J.R.R. Tolkien"},
    {"book_id": 8, "name": "Moby-Dick", "author": "Herman Melville"},
    {"book_id": 9, "name": "War and Peace", "author": "Leo Tolstoy"},
    {"book_id": 10, "name": "The Chronicles of Narnia", "author": "C.S. Lewis"},
]


# Function to insert books into the database
def insert_books_into_db():
    with app.app_context():
        # Check if any books already exist in the database
        existing_books = bookModel.query.all()
        existing_book_names = {book.name for book in existing_books}

        for book_info in famous_books:
            # Check if the book already exists in the database
            if book_info["name"] not in existing_book_names:
                book = bookModel(name=book_info["name"], author=book_info["author"])
                db.session.add(book)
        db.session.commit()


insert_books_into_db()


# Resource for LISTING all books and CREATE new book
class Books(Resource):
    def get(self):
        books = bookModel.query.all()
        book_list = []
        for book in books:
            book_data = book.to_dict()
            book_list.append(book_data)
        return jsonify(book_list)

    def post(self):
        data = request.get_json(self)

        new_book = bookModel(name=data["name"], author=data["author"])
        db.session.add(new_book)
        db.session.commit()
        return {"Massage": "Book has been added"}, 201


# Resource for LISTING indivduell book or DELETE book by ID
class Book(Resource):
    def get(self, id):
        book = bookModel.query.get(id)
        if book:
            return book.to_dict(), 200
        else:
            return {"massage": "Book not found"}, 404

    def delete(self, id):
        bookTodelete = bookModel.query.filter_by(id=id).first()
        if bookTodelete:
            db.session.delete(bookTodelete)
            db.session.commit()
            return "Book has been DELETED"
        else:
            return "Book not found"


api.add_resource(Books, "/books")  # API Endpoint
api.add_resource(Book, "/book/<int:id>")  # API Endpoint


"""@app.route("/books", methods=["GET"])
def print():
    return jsonify(famous_books)


@app.route("/<name>")
def print_name(name):
    return jsonify("Hallo {}".format(name))"""


if __name__ == "__main__":
    app.run(debug=True)
