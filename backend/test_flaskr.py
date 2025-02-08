import unittest
import json
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

        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

        self.new_question = {
            "question": "What is the capital of France?",
            "answer": "Paris",
            "category": "3",
            "difficulty": 1
        }

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    """
    def test_get_categories(self):
        res = self.client.get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["categories"])

    def test_get_questions_paginated(self):
        res = self.client.get("/questions?page=1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
"""
    def test_get_questions_beyond_valid_page(self):
        res = self.client.get("/questions?page=1000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], 404)

    def test_delete_question(self):
        question = Question(**self.new_question)
        with self.app.app_context():
            db.session.add(question)
            db.session.commit()
            question_id = question.id

        res = self.client.delete(f"/questions/{question_id}")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_non_existing_question(self):
        res = self.client.delete("/questions/10000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], 404)

    def test_create_question(self):
        res = self.client.post("/questions", json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["created"])
    """
    def test_create_question_with_missing_fields(self):
        res = self.client.post("/questions", json={})
        print(res.status_code, res.data)  # Check what response is actually returned
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["error"], 400)
    """
    def test_search_questions(self):
        self.client.post("/questions", json=self.new_question)
        res = self.client.post("/questions/search", json={"searchTerm": "capital"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]) > 0)

    def test_search_questions_not_found(self):
        res = self.client.post("/questions/search", json={"searchTerm": "xyzxyzxyz"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data["questions"]), 0)
    """
    def test_get_questions_by_category(self):
        res = self.client.get("/categories/1/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]) > 0)
    """
    def test_get_questions_by_invalid_category(self):
        res = self.client.get("/categories/999/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], 404)

    def test_play_quiz(self):
        res = self.client.post("/quizzes", json={
            "previous_questions": [],
            "quiz_category": {"id": 1}
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("question" in data)
    """
    def test_play_quiz_invalid_category(self):
        res = self.client.post("/quizzes", json={
            "previous_questions": [],
            "quiz_category": {"id": 999}
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], 404)
    """
if __name__ == "__main__":
    unittest.main()
