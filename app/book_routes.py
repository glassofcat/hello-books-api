from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, abort, make_response, request

# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description

#     def to_json(self):
#         return {
#                 "id": self.id,
#                 "title": self.title,
#                 "description": self.description
#                     }
    

# books = [
#     Book(1, "Fashon", "pretty stuff"),
#     Book(2, "Romance", "ooo steamy"),
#     Book(3, "Bakeing", "sugar hi o/")
# ]



books_bp = Blueprint("books", __name__, url_prefix="/books")



def validate_book(book_id):
        try:
            book_id = int(book_id)
        except:
            abort(make_response({"message": f"book {book_id} is invalid"}, 400))
        
        book = Book.query.get(book_id)

        if not book:
            abort(make_response(jsonify({"message": f"book {book_id} not found"}), 404))
        return book

        # for book in books:
        #     if book.id == book_id:
        #         return book_id

        # abort(make_response({"message": f"book {book_id} not found"}, 404))

@books_bp.route("", methods=["POST"])
def write_books():
    request_body = request.get_json()
    new_book = Book(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)


@books_bp.route("", methods=["GET"])
def read_all_books():

    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()

    books_response = []
    for book in books:
        books_response.append(book.to_json())
    return jsonify(books_response)

@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    book = validate_book(book_id)
    return book.to_json(), 200

@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()
    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully updated"))

@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_book(book_id)
    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully deleted"))
