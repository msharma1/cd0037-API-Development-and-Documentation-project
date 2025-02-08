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
    app = Flask(__name__)
    setup_db(app, test_config.get('SQLALCHEMY_DATABASE_URI') if test_config else None)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = {category.id: category.type for category in Category.query.all()}
        return jsonify({'success': True, 'categories': categories})

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

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = db.session.get(Question, question_id)
        if question is None:
            abort(404)
        question.delete()
        return jsonify({'success': True, 'deleted': question_id})

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

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        search_term = request.get_json().get('searchTerm', '')
        if search_term:
            selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            return jsonify({'success': True, 'questions': paginate_questions(request, selection), 'total_questions': len(selection)})
        abort(422)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)
        if category is None:
            abort(404)
        selection = Question.query.filter(Question.category == str(category_id)).all()
        return jsonify({'success': True, 'questions': paginate_questions(request, selection), 'total_questions': len(selection), 'current_category': category.type})

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

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'error': 404, 'message': 'Resource not found'}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({'success': False, 'error': 422, 'message': 'Unprocessable entity'}), 422

    return app
