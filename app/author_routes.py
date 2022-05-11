from app import db
from app.models.author import Author
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.book import Book

authors_bp = Blueprint("authors", __name__, url_prefix="/authors")

def validate_author(author_id):
        try:
            author_id = int(author_id)
        except:
            abort(make_response({"message": f"author {author_id} is invalid"}, 400))
        
        author = Author.query.get(author_id)

        if not author:
            abort(make_response(jsonify({"message": f"author {author_id} not found"}), 404))
        return author

@authors_bp.route("", methods=["POST"])
def write_author():
    request_body = request.get_json()
    new_author = Author(name=request_body["name"])

    db.session.add(new_author)
    db.session.commit()

    return make_response(jsonify(f"Author {new_author.name} successfully created"), 201)

@authors_bp.route("/<id>/books", methods=["POST"])
def write_book_to_author(id):
    author = validate_author(id)
    request_body = request.get_json()
    new_book = Book(title=request_body["title"], description=request_body["description"], author=author)

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} by author {new_book.author.name} successfully created"), 201)

@authors_bp.route("/<id>/books", methods=["GET"])
def read_all_books(id):

    # name_query = request.args.get("name")
    # if name_query:
    #     authors = Author.query.filter_by(name=name_query)
    # else:
    author = validate_author(id)

    books_response = []
    for book in author.books:
        books_response.append(book.to_json())
    return jsonify(books_response)

    

# authors_bp = Blueprint("authors_bp", __name__, url_prefix="/authors")