import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
# db_drop_and_create_all()
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,PATCH')
    return response

## ROUTES
@app.route("/drinks", methods = ["GET"])
def get_drinks():
    try:
        drinks = Drink.query.all()
        drinks = [d.short() for d in drinks]
        return jsonify({
            "success": True,
            "drinks": drinks
        })
    except:
        abort(404)


@app.route("/drinks-details", methods=['GET'])
@requires_auth("get:drinks-details")
def get_drinks_detail(token):
    drinks = Drink.query.all()
    # print(drinks)
    try:
        
        drinks = [d.long() for d in drinks]
        return jsonify({
            "success": True,
            "drinks": drinks
        })

    except Exception:
        print('exception')
        abort(404)


@app.route("/drinks", methods=['POST'])
@requires_auth("post:drinks")
def create_drinks(token):
    body = request.get_json()

    if not ('title' in body and 'recipe' in body):
        abort(422)

    new_drink_title = body.get('title', None)
    new_drink_recipe = body.get('recipe', None)

    try:
        new_drink = Drink(
            title=new_drink_title,
            recipe=json.dumps(new_drink_recipe))
        new_drink.insert()

        return jsonify({
            'success': True,
            'drinks': [new_drink.long()]
        })
    except:
        abort(422)


@app.route("/drinks/<int:id>", methods = ["PATCH"])
@requires_auth("patch:drinks")
def update_drinks(token, id):
    body = request.get_json()
    drink = Drink.query.get(id)
    if drink :
        try:
            update_title = body.get("title",None)
            update_recipe = body.get("recipe", None)
            if update_title:
                drink.title = update_title

            if update_recipe:
                drink.recipe = update_recipe

            drink.update()
            return jsonify({
                'success': True,
                'drinks': [drink.long()]
            })
        except:
            abort(422)

    else:
        abort(404)


@app.route("/drinks/<int:id>",methods =["DELETE"])
@requires_auth("delete:drinks")
def delete_drinks(token, id):

    drink = Drink.query.filter(Drink.id == id).one_or_none()

    try:
        if not drink:
            abort(404)
        drink.delete()

        return jsonify({
            "success":True,
            "delete": id
        })

    except:
        abort(422)



## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

@app.errorhandler(400)
def error_400_bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


@app.errorhandler(404)
def error_404_not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


@app.errorhandler(500)
def error_500_internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500



@app.errorhandler(AuthError)
def error_Authorization(err):
    response = jsonify(err.error)
    response.status_code = err.status_code
    return response

