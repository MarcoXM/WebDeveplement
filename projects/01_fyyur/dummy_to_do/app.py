from flask import Flask, render_template,url_for,redirect, request, jsonify,abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sqlmarco:4mysiri@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app=app, db=db)

class TODOtable(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer(), primary_key = True)
    description = db.Column(db.String(), nullable = False)
    completed = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__ (self, ):
        return f" TO DO: {self.id} {self.description}"
db.create_all()

@app.route("/todos/create", methods=['POST'])
def create_todos():
    error = False
    body = {}
    try:
        description = request.form.get_json()['description']
        todo = TODOtable(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort (400)
        pass
    else:
        return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
  try:
    completed = request.get_json()['completed']
    print('completed', completed)
    todo = TODOtable.query.get(todo_id)
    todo.completed = completed
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))

# INSERT INTO todos (description) VALUES ('python');
# INSERT INTO todos (description) VALUES ('golang');
# INSERT INTO todos (description) VALUES ('cpp');
@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        TODOtable.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({ 'success': True })



@app.route("/")
def index():

    return render_template("index.html", data = TODOtable.query.all())


if __name__ == "__main__":
    app.run(debug=True)