from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Boolean,Integer, create_engine
from config import SQLALCHEMY_DATABASE_URI
import os 
import json

db = SQLAlchemy()

def setup_db(app, db_path = SQLALCHEMY_DATABASE_URI):
    '''
    Set up envionment and connect to the database
    '''

    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Book(db.Model):
    '''
    Build up a bookstore database, this is the book table
    
    '''
    __tablename__ = "books"

    id = Column(Integer, primary_key= True, nullable=False)
    name = Column(String)
    author = Column(String)
    genre = Column(String)

    def __init__(self,name, author, genre):
        self.name = name
        self.author = author
        self.genre = genre

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):

    # return the json format for each book infomation

        return {
            "id" : self.id,
            "name" : self.name,
            "author" : self.author,
            "genre" : self.genre,
        }



