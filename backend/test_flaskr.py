import os
import unittest
import json
from flaskr import create_app
from models import setup_db, Question, Category, db

class TriviaTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_questions(self):
        """Test getting paginated questions"""
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_sent_requesting_beyond_valid_page(self):
        """Test 404 error when requesting beyond valid page"""
        response = self.client().get('/questions?page=1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['success'] == False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_question(self):
        """Test creating a new question"""
        new_question = {
            'question': 'What is the capital of France?',
            'answer': 'Paris',
            'category': 1,
            'difficulty': 1
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])

    def test_422_create_question(self):
        """Test 422 error when creating a question with missing data"""
        new_question = {
            'question': 'What is the capital of France?',
            'answer': 'Paris'
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertTrue(data['success'] == False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_question(self):
        """Test deleting a question"""
        # First, create a question to delete
        new_question = {
            'question': 'What is the capital of Germany?',
            'answer': 'Berlin',
            'category': 1,
            'difficulty': 1
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        question_id = data['created']

        # Now, delete the question
        response = self.client().delete(f'/questions/{question_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['deleted'])

    def test_404_delete_question(self):
        """Test 404 error when deleting a non-existent question"""
        response = self.client().delete('/questions/1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['success'] == False)
        self.assertEqual(data['message'], 'resource not found')

if __name__ == "__main__":
    unittest.main()