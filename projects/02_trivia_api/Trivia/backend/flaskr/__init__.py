import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate(request, selections):
    page = request.args.get('page', 1, type=int)
    start_idx = (page - 1) * QUESTIONS_PER_PAGE 
    end_idx = start_idx + QUESTIONS_PER_PAGE

    format_result = [ b.format() for b in selections]
    return format_result[start_idx:end_idx]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
  
    ## Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    cors = CORS(app=app, resource = (r"/api/*":{"origin" :"*"}))


    ## Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
    @app.route("/categories", methods=['GET'])
    def get_categories_info():
        cate_resutls = Category.query.order_by(Category.id).all()
        cates = paginate(request=request, selections=cate_resutls)

        if not cates:
            abort(404)

        else:
            return jsonify({
                "successs": True,
                "total_categories":len(cate_resutls),
                "categories":cates
            })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
    @app.route("/questions", methods=['GET'])
    def get_questions():
        questions_selection = Question.query.order_by(Question.id).all()
        current_questions = paginate(request, questions_selection)

        if not current_questions:
            abort(404)

        else:
            return jsonify({
                "success":True,
                "total_questions":len(questions_selection),
                "questions":current_questions
            })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
    @app.route("/questions/<int:question_id>", methods = ['DELETE'])
    def delete_question(question_id):

        body = request.get_json()

        try:
            questions = Question.query.filter(Question.id = question_id).one_or_none()
            if not questions:
                abort(404)

            Question.delete()
            ## show result 
            questions_selection = Question.query.order_by(Question.id).all()
            current_questions = paginate(request,questions_selection)

            ## jsonify to the view
            return jsonify({
                "success":True,
                "deleted_question_id":question_id,
                "total_questions":len(questions_selection),
                "questions": current_questions
            })
        except:
            abort(500)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
    @app.route("/questions", methods=['POST'])
    def create_question():
        try:
            body = request.get_json()
            question_text = body['question']
            question_answer = body['answer']
            question_cate = body['category']
            question_difficulty = body['difficulty']

            question = Question(question=question_text,answer=question_answer,category=question_cate,difficulty=question_difficulty)
            question.insert()

            return jsonify({
                    'success': True,
                    'message': 'Question added successfully'
                })
        except ValueError:
            print(sys.exc_info())
            abort(500)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
    @app.route("/questions", methods=["POST"])
    def search_questions():
        body = request.get_json()
        question_text = body['question']
        question_answer = body['answer']
        question_cate = body['category']
        question_difficulty = body['difficulty']
        search = body['searchTerm']

        try:
            questions_selection = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search)))
            if len(questions_selection) == 0:
                return abort(404)
            current_questions = paginate(request,questions_selection)
            return jsonify({
                "success":True,
                "total_questions":len(questions_selection),
                "question":current_questions,
            })
        except:
            abort(404)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
    @route("/categories/<int:category_id>/question", method=['GET'])
    def get_question_by_category(category_id):
        body = request.get_json()

        try: # with_type == select
            cates_text = Category.query.with_entities(Category.type).filter_by(id=category_id).one_or_none()
            if cates_text is None:
                return abort(404)

            questions = Question.query.with_entities(Question,Category.type).join(Category, Category.id == Question.category)\
            .filter(Category.id == category_id).all()

            if not question:
                return abort(404)

            create_question = paginate(request,questions)
            return jsonify({
                'success': True,
                'questions': create_question,
                'total_questions': len(questions),
                'current_category': cates_text[0]
            })
        except:
            abort(404)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
    @app.route("/quiz", methods=["POST"])
    def play_quiz():
        body = request.get_json()
        prev_questions = body['previous_questions']
        qc_type = body['quiz_category']['type']
        qc_id = body['quiz_category']['type_id']
        if qc_id == 0:
            questions = Question.query.all()
            question = random.choice(questions)
        else:
            questions = Question.query.filter(Question.category == qc_id).all()
            question = random.choice(questions)

        return jsonify({
            "success":True,
            "previous_question":prev_questions,
            "question":questions.format() if questions else ""
        })

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
    def error_400_bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def error_404_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def error_422_Unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422

    @app.errorhandler(500)
    def error_500_internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500
  
  return app

    
  