from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random
from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    return questions[start:end]

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    """
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})
    with app.app_context():
        db.create_all()
    """
    @DONE: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        return response
    """
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = {category.id: category.type for category in Category.query.all()}
        return jsonify({'success': True, 'categories': categories})

    """
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.all()
        paginated_questions = paginate_questions(request, selection)
        if len(paginated_questions) == 0:
            abort(404)
        categories = {category.id: category.type for category in Category.query.all()}
        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(selection),
            'categories': categories,
            'current_category': None
        })

    """
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = db.session.get(Question, question_id)
        if question is None:
            abort(404)
        question.delete()
        return jsonify({'success': True, 'deleted': question_id})

    """
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()
        question_text = data.get('question')
        answer = data.get('answer')
        category = data.get('category')
        difficulty = data.get('difficulty')
        if not (question_text and answer and category and difficulty):
            abort(400, description="Missing required fields")
        question = Question(question=question_text, answer=answer, category=category, difficulty=difficulty)
        question.insert()
        return jsonify({'success': True, 'created': question.id}), 201

    """
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        search_term = request.get_json().get('searchTerm', '')
        if search_term:
            selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            return jsonify({'success': True, 'questions': paginate_questions(request, selection), 'total_questions': len(selection)})
        abort(422)

    """
    @DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)
        if category is None:
            abort(404)
        selection = Question.query.filter(Question.category == str(category_id)).all()
        return jsonify({'success': True, 'questions': paginate_questions(request, selection), 'total_questions': len(selection), 'current_category': category.type})

    """
    @DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        data = request.get_json()
        category_id = data.get('quiz_category', {}).get('id')
        previous_questions = data.get('previous_questions', [])
        query = Question.query
        if category_id:
            query = query.filter(Question.category == str(category_id))
        questions = query.filter(Question.id.notin_(previous_questions)).all()
        return jsonify({'success': True, 'question': random.choice(questions).format() if questions else None})

    """
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'error': 404, 'message': 'Resource not found'}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({'success': False, 'error': 422, 'message': 'Unprocessable entity'}), 422

    return app
