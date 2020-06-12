# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 



#### REVIEW_COMMENT

##### Endpoints

```json
get categoies : GET '/categories'  
get questions : GET '/questions'
get questions by cate : GET '/categories/<category_id>/questions'
search questions : POST '/questions/search'
add new questions : POST '/questions/add'
start quiz : POST '/quizzes'
delete questions : DELETE '/questions/<question_id>'
```

##### Details

1. GET '/categories'

```json
Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

Request Arguments: None

Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
        {'1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"}
```

2. GET '/questions'

```json
Fetches all the quesitons. If a category argument is provided then it returns the questions of the selected category.
  The query is paginated to return 10 questions per page if a page argument is provided.   
- Request Arguments: category, page
- Returns: A json object with success, questions, total_questions, current_category, categories that contains key:value pairs. 

GET '/categories/<category_id>/questions'
- Fetches all the questions of a selected category. 
- Request Arguments: None
- Returns: A json object conatining current_catergory with all the questions from the selected category.
{
  "current_category": "Geography",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

POST '/questions/search'
```json
- Fetches all the questions that matches the searchTerm.
- Request Arguments: searchTerm
- Returns: A json object containing all the questions that matches the search term.
{
   'success': True,
   'current_category':question's cate type,
   'total_questions': 10,
   'questions': current_questions_get
}
```

POST '/questions/add'
```json
- Creates a new question into the database.
- Request Arguments: None
- Returns: A json object specifying the success and message. 
{
  'success': True,
  'message': 'Question added successfully'
}
```

POST '/quizzes'
```json
- Gets a question from the database based on the selected category.
- Request Arguments: json object containing previous_questions, current_questions, category.
- Returns: A question from the selected category.
{
previousQuestions: [],
question: {
            answer: 'Apollo 13',
            category: 5,
            difficulty: 4,
            id: 2,
            question: 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?'
          },
success: True
}
```

DELETE '/questions/<question_id>'
```json
- Deletes the selected question from the database.
- Request Arguments: None
- Returns: A json object specifying the success and message. 
{
   'success': True,
   'deleted_question_id':question_id,
   'total_questions': 10,
   'questions': current_questions_left
}
```




## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```