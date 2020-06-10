from flask import jsonify, Flask, request, abort
from flask_cors import CORS
from sqlmodel import setup_db, Book




def paginate_book(request,selections):
    page = request.args.get('page', 1, type=int)
    start_idx = (page - 1) * 10 
    end_idx = start_idx + 10

    books = [ b.format() for b in selections]
    return books[start_idx:end_idx]


def create_app(test_config=None):

    ### initize the flask app 
    app = Flask(__name__)
    setup_db(app)
    ### initialize flask cors
    cors = CORS(app, 
                resources={r"/api/*": {"origins": "*"}})

    # CORS Headers  setting the cors
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    

    ### getting the total infomations of the books in the store

    @app.route('/books',methods=['GET'])
    def get_books_info():
        
        selections = Book.query.order_by(Book.id).all()
        books = paginate_book(request = request, selections = selections)

        if not books:
            abort(404)

        else:
            return jsonify({
                'sussess': True,
                'total books' : len(selections),
                'book info': books
            })


    #### get one book info
    @app.route('/books/<int:book_id>')
    def get_spesific_book(book_id):

        book = Book.query.filter(Book.id==book_id).one_or_none()

        if book is None:
            abort(404)
        else:
            return jsonify({
                'success' : True,
                "book_info":book.format()
            })

    @app.route('/books/<int:book_id>', methods = ['PATCH'])
    def update_book(book_id):
        '''
        curl -X PATCH http://127.0.0.1:5000/books/1 -H "Content-Type: application/json" -d '{"name":"Harry Potter"}' 
        '''
        body = request.get_json()
        try:
            book = Book.query.filter(Book.id==book_id).one_or_none()
            if not book:
                abort(404)
            if body.get('name'):
                book.name = body.get('name')
            if body.get('author'):
                book.author = body.get('author')
            if body.get('genre'):
                book.genre = body.get('genre')
            book.update()
            return jsonify({
                'success': True,
                "id": book.book_id
            })
        except:
            abort(404)
    @app.route('/books/<int:book_id>', methods = ['DELETE'])
    def delete_book(book_id):
        '''
        curl -X PATCH http://127.0.0.1:5000/books/1 -H "Content-Type: application/json" -d '{"name":"Harry Potter"}' 
        '''
        body = request.get_json()
        try:
            book = Book.query.filter(Book.id==book_id).one_or_none()
            if not book:
                abort(404)

            book.delete()

            selections = Book.query.order_by(Book.id).all()
            current_books = paginate_book(request,selections)

            return jsonify({
                'success': True,
                "deleted": book_id,
                "books info " : current_books,
                "total_books":len(selections)
            })
        except:
            abort(404)

    @app.route('/books', methods = ['POST'])
    def create_book():
        '''
        curl -X PATCH http://127.0.0.1:5000/books/1 -H "Content-Type: application/json" -d '{"name":"Harry Potter"}' 
        '''
        body = request.get_json()
        book_name = body.get('name')
        book_author = body.get('author')
        book_genre = body.get('genre')
        search = body.get('search',None)

        try:
            if search :
                selections = Book.query.order_by(Book.id).filter(Book.name.ilike("%{}%".format(search)))
                current_books = paginate_book(request,selections)
                return jsonify({
                    'success': True,
                    "inserted": Book.id,
                    "books info " : current_books,
                    "total_books":len(selections)
                })

            else:
                book = Book(name=book_name,author=book_author,genre=book_genre)
                book.insert()

                selections = Book.query.order_by(Book.id).all()
                current_books = paginate_book(request,selections)

                return jsonify({
                    'success': True,
                    "inserted": book.id,
                    "books info " : current_books,
                    "total_books":len(selections)
                })
        except:
            abort(422)


    #### error handling 
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Not found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

    ## return flask app
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)