import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys
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
    cors = CORS(app=app, resource = {r"/api/*" : {"origin":"*"}})


    ## Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response


    @app.route("/categories", methods=['GET'])
    def get_categories_info():
        cate_resutls = Category.query.order_by(Category.id).all()
        cates = paginate(request=request, selections=cate_resutls)

        if not cates:
            abort(404)

        else:
            return jsonify({
                "success": True,
                "total_categories":len(cate_resutls),
                "categories":cates
            })



    @app.route("/questions", methods=['GET'])
    def get_questions():
        questions_selection = Question.query.order_by(Question.id).all()
        current_questions = paginate(request, questions_selection)

        if not current_questions:
            abort(422)

        else:
            return jsonify({
                "success":True,
                "total_questions":len(questions_selection),
                "questions":current_questions
            })


    @app.route("/questions/<int:question_id>", methods = ['DELETE'])
    def delete_question(question_id):
        body = request.get_json()
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if not question:
                abort(404)

            question.delete()
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


    @app.route("/questions/add", methods=['POST'])
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

    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        body = request.get_json()
        # question_text = body['question']
        # question_answer = body['answer']
        # question_cate = body['category']
        # question_difficulty = body['difficulty']
        search = body['searchTerm']
        try:
            questions_selection = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search))).all()
            if len(questions_selection) == 0:
                return abort(404)
            current_questions = paginate(request,questions_selection)
            return jsonify({
                "success":True,
                "total_questions":len(questions_selection),
                "questions":current_questions,
            })
        except:
            abort(404)


    @app.route("/categories/<int:category_id>/questions", methods=['GET'])
    def get_question_by_category(category_id):
        body = request.get_json()

        try: # with_type == select
            cates_text = Category.query.with_entities(Category.type).filter_by(id=category_id).one_or_none()

            if cates_text is None:
                return abort(404)

            questions = Question.query.with_entities(Question,Category.type).join(Category, Category.id == Question.category)\
            .filter(Category.id == category_id).all()


            ## questions > (question ,tag )
            if not questions:
                return abort(404)
            create_question = [q.Question.format() for q in questions]

            return jsonify({
                'success': True,
                'questions': create_question,
                'total_questions': len(questions),
                'current_category': cates_text[0]
            })
        except:
            abort(404)


    @app.route("/quiz", methods=["POST"])
    def play_quiz():
        body = request.get_json()
        prev_questions = body['previous_questions']
        previous_ids = [q['id'] for q in prev_questions] if prev_questions else []
        qc_type = body['quiz_category']['type']
        qc_id = body['quiz_category']['type_id']
        random.seed(224)
        if qc_id == 0:
            questions = Question.query.all()
            while True:
                question = random.choice(questions)
                if question.id in previous_ids:
                    continue
                else:
                    break
        else:
            questions = Question.query.filter(Question.category == qc_id).all()
            while True:
                question = random.choice(questions)
                if len(prev_questions) == len(questions):
                    question = ''
                    break
                elif question.id in previous_ids:
                    continue
                else:
                    break
                
        return jsonify({
            "success":True,
            "previous_questions":prev_questions,
            "question":question.format() if question else ""
        })


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

    
if __name__ =="__main__":
    app = create_app()
    app.run(debug=True)