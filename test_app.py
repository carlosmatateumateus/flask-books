import unittest
import tempfile
import os

from flaskr import init_db
from app import app

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.client = app.test_client()

        init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_books(self):
        '''
        CRUD BOOK
        '''

        rv = self.client.post('/create', json={
            "title": "Lobos",
            "description": "Lobos",
            "price": 240.32,
        })

        self.assertEqual(rv.status_code, 201)

        books = self.client.get('/')

        self.assertEqual(books.status_code, 200)

        rv = self.client.get('/read/1')
        self.assertEqual(rv.status_code, 200)

        rv = self.client.put('/update/1', json={
            "title": "Cães",
            "description": "Cães",
            "price": 40.67,
        })

        self.assertEqual(rv.status_code, 202)   

    def test_delete_book(self):
        '''
        DELETE BOOK
        '''
        book = self.client.delete('/delete/122')

        self.assertEqual(book.status_code, 200)


if __name__ == '__main__':
    unittest.main()