import os
import unittest

from flaskr import create_app
from models import db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_user = "postgres"
        self.database_password = "password"
        self.database_host = "localhost:5432"
        self.database_path = f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}/{self.database_name}"

        # Create app with the test configuration
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        # Bind the app to the current context and create all tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        """Test getting categories"""
        response = self.client.get("/categories")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["categories"])
    
    def test_404_sent_requesting_beyond_valid_page(self):
        """Test 404 error when requesting beyond valid page"""
        response = self.client.get("/questions?page=1000")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")

    def test_get_questions(self):
        """Test getting questions"""
        response = self.client.get("/questions")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertTrue(data["current_category"])

    def test_delete_question(self):
        """Test deleting a question"""
        question = Question(question="Test question", answer="Test answer", difficulty=1, category=1)
        question.insert()

        response = self.client.delete(f"/questions/{question.id}")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["deleted"], question.id)

    def test_404_delete_question(self):
        """Test 404 error when deleting a non-existing question"""
        response = self.client.delete("/questions/1000")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")

    def test_create_question(self):
        """Test creating a question"""
        question = {
            "question": "Test question",
            "answer": "Test answer",
            "difficulty": 1,
            "category": 1
        }

        response = self.client.post("/questions", json=question)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["created"])

    def test_422_create_question(self):
        """Test 422 error when creating a question with missing data"""
        question = {
            "question": "Test question",
            "difficulty": 1,
            "category": 1
        }

        response = self.client.post("/questions", json=question)
        data = response.get_json()

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unprocessable")

    def test_search_questions(self):
        """Test searching questions"""
        search = {"searchTerm": "test"}

        response = self.client.post("/questions/search", json=search)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def test_get_questions_by_category(self):
        """Test getting questions by category"""
        response = self.client.get("/categories/1/questions")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
