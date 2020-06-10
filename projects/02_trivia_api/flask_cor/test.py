import unittest
import os
import json
from config import *

from app import create_app
from sqlmodel import setup_db,Book

class BookTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client ## this is from the flask class call
        self.test_db_name = "book_test"
        self.test_db_path = f'{DATABASE}://{USERNAME}{PASSWORD}@{HOST}:{PORT}/{self.test_db_name}'

        ## initial app with db
        setup_db(self.app, db_path=self.test_db_path)

        self.new_book = {
            "name" : "magic ingredients",
            "author":"Miss Gao",
            "Genre" : "Cooking"
        }

    def testProcess(self):
        pass

    def test_get_pagenate_books(self):
        res = self.client().get("/books")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total books"])
        self.assertTrue(len(data["book info"]))


    def test_404_sent_page_beyond(self):
        res = self.client().get("/books?page=1000", json ={ "genre" : "food"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"],"Not found")


    def test_update_book_author(self):

        res = self.client().get("/books/5", json = {"author": "Me"})
        data = json.loads(res.data)
        book = Book.query.filter(Book.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(book.format()["author"],"Me")
    
    def test_create_book(self, new_book = self.new_book):
        pass


# Write test for specific application behavior.
# Run the tests and watch them fail.
# Write code to execute the required behavior.
# Test the code and rewrite as necessary to pass the test
# Refactor your code.
# Repeat - write your next test.