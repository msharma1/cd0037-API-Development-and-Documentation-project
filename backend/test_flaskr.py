import unittest
import json
from flaskr import create_app
from models import db, Question, Category
from settings import DB_USER, DB_PASSWORD
from sqlalchemy import text

# Database configuration
database_name = "trivia_test"
database_path = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{database_name}'

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Add sample categories
            category = Category(type="Science")
            db.session.add(category)
            db.session.commit()

            # Add sample questions
            self.new_question = {
                "question": "What is the capital of France?",
                "answer": "Paris",
                "category": str(category.id),  # Ensure category.id is correctly passed as a string
                "difficulty": 1
            }

            question = Question(**self.new_question)
            db.session.add(question)
            db.session.commit()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            with db.engine.connect() as connection:
                connection.execute(text("DROP TABLE IF EXISTS questions CASCADE;"))
                connection.execute(text("DROP TABLE IF EXISTS categories CASCADE;"))
            db.drop_all()

    ## --------------------- GET Requests ---------------------

    def test_get_categories_success(self):
        res = self.client.get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["categories"])

    def test_get_categories_failure(self):
        res = self.client.get("/invalid_categories")
        self.assertEqual(res.status_code, 404)

    def test_get_questions_success(self):
        res = self.client.get("/questions?page=1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def test_get_questions_failure(self):
        res = self.client.get("/questions?page=1000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], 404)

    ## --------------------- POST Requests ---------------------

    def test_create_question_success(self):
        res = self.client.post("/questions", json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["created"])

    def test_create_question_failure(self):
        res = self.client.post("/questions", json={})  # Sending empty JSON body

        print("Response Status:", res.status_code)
        print("Response Data:", res.data.decode("utf-8"))

        if res.headers.get("Content-Type") != "application/json":
            self.fail("API did not return JSON response.")

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["error"], 400)
        self.assertEqual(data["message"], "Missing required fields")

    def test_search_questions_success(self):
        self.client.post("/questions", json=self.new_question)
        res = self.client.post("/questions/search", json={"searchTerm": "capital"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]) > 0)

    def test_search_questions_failure(self):
        res = self.client.post("/questions/search", json={"searchTerm": "xyzxyzxyz"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data["questions"]), 0)

    def test_get_questions_by_category_success(self):
        res = self.client.get("/categories/1/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]) > 0)

    def test_get_questions_by_category_failure(self):
        res = self.client.get("/categories/999/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], 404)

    ## --------------------- DELETE Requests ---------------------

    def test_delete_question_success(self):
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

    ## --------------------- Quiz Game ---------------------

    def test_play_quiz_success(self):
        res = self.client.post("/quizzes", json={
            "previous_questions": [],
            "quiz_category": {"id": 1}
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("question" in data)

    def test_play_quiz_failure(self):
        res = self.client.post("/quizzes", json={"previous_questions": [], "quiz_category": {"id": 999}})
        
        # Debugging print
        print("Quiz Failure Response:", res.status_code, res.data.decode("utf-8"))

        if res.headers.get("Content-Type") != "application/json":
            self.fail("API did not return JSON response.")

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Category not found")

if __name__ == "__main__":
    unittest.main()
