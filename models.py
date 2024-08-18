from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import unittest
from app import create_app, db
from app.models import Book

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_book(self):
        response = self.client.post('/books', json={
            'title': 'Sample Book',
            'author': 'Author Name',
            'published_date': '2024-01-01',
            'ISBN': '1234567890123'
        })
        self.assertEqual(response.status_code, 201)

    def test_get_book(self):
        book = Book(title='Sample Book', author='Author Name', published_date='2024-01-01', ISBN='1234567890123')
        with self.app.app_context():
            db.session.add(book)
            db.session.commit()
        
        response = self.client.get(f'/books/{book.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sample Book', str(response.data))

if __name__ == '__main__':
    unittest.main()

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.Date, nullable=False)
    ISBN = db.Column(db.String(13), unique=True, nullable=False)
    availability = db.Column(db.Boolean, default=True)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    membership_date = db.Column(db.Date, default=datetime.utcnow)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    borrow_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.Date, nullable=True)
