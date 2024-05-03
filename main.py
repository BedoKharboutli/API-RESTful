from flask import Flask, jsonify, request, json, session
import requests
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

# Create a Flask Instance
app = Flask(__name__)
# Connect app to API
api = Api(app)
db = SQLAlchemy()

# Configuration for SQLite database with file name (Case.db)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Case.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# initalize the databse on the app
db.init_app(app)


# Create table...
class bookModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)

    # Function that returns data as JSON
    def to_dict(self):
        return {"name": self.name, "author": self.author, "id": self.id}


# Create tables if not exists
with app.app_context():
    db.create_all()

# some books to insert into database later
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


# Resource for listing all books from database and CREATE new book
class Books(Resource):
    def get(self):
        books = bookModel.query.all()
        book_list = []
        for book in books:
            book_data = book.to_dict()
            book_list.append(book_data)
        return {"StatusCode": 200, "Books": book_list}

    def post(self):
        data = request.get_json(self)

        new_book = bookModel(name=data["name"], author=data["author"])
        db.session.add(new_book)
        db.session.commit()
        # return {"STATUS CODE : 201 Created | Massage": "Book has been added"}, 201
        return {
            "StatusCode": 201,
            "Message": "Book was succesfully created",
            "book": new_book.to_dict(),
        }, 201


# Resource for listing indivduell book from database or DELETE book by ID from database
class Book(Resource):
    def get(self, id):
        book = bookModel.query.get(id)
        if book:
            return book.to_dict(), 200
        else:
            return {"massage": "Book not found"}, 404

    def delete(self, id):
        bookTodelete = bookModel.query.get(id)
        if bookTodelete:
            db.session.delete(bookTodelete)
            db.session.commit()
            """return "Book has been DELETED", 200"""
            return {
                "StatusCode": 200,
                "Massage": "Book has been DELETED",
                "book": bookTodelete.to_dict(),
            }
        else:
            return {"Massage": "Book not found", "StatusCode": 404}


OPEN_LIBRARY_API_URL = "http://openlibrary.org/search.json"


# Resource for listing books from OPEN_LIBRARY_API by searching name
class Search_book(Resource):
    def get(self, name):
        # Make a request to the Open Library API
        URL = f"{OPEN_LIBRARY_API_URL}?q={name}"
        response = requests.get(URL)

        if response.status_code == 200:
            data = response.json()
            books = data.get("docs", [])
            # Create a list with details for each book
        for book in books:
            book_details = {
                "title": book.get("title", ""),
                "author": book.get("author_name")[0],  # Get author's name (first)
                "publish_year": book.get("publish_year")[0],
            }

            return jsonify({"StatusCode": 200, "book": book_details})
        else:
            return jsonify({"StatusCode": 403, "error": "Failed to fetch books"})


# Resource for showing the JSON file with the api-documentation in it
class Show_api_documentation(Resource):
    def get(self):
        with open("API_docs.json", "r") as file:
            api_documentation = json.load(file)
        return api_documentation


api.add_resource(Books, "/books")  # API Endpoint
api.add_resource(Search_book, "/books/<string:name>")  # API Endpoint
api.add_resource(Book, "/book/<int:id>")  # API Endpoint
api.add_resource(Show_api_documentation, "/api/docs")  # API Endpoint


if __name__ == "__main__":
    app.run(debug=True)
