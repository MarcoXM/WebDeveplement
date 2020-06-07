from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sqlmarco:4mysiri@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



@app.route("/")
def hello_world():
    person = Person.query.first()
    return 'Hello ' + person.name
   
    
class Person(db.Model):
    __tablename__ = "persons"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.name}>'


db.create_all()


if __name__ == "__main__":
    app.run(debug = True)