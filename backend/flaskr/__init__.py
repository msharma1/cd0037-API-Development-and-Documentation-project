from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/questions')
    def get_questions():
        try:
            page = request.args.get('page', 1, type=int)
            questions = Question.query.paginate(page, QUESTIONS_PER_PAGE, False)

            if questions.items == []:
                abort(404)

            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions.items],
                'total_questions': questions.total,
                'current_category': 'All'  # Set a default value for current_category
            })
        except Exception as e:
            print(e)
            abort(500)

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        if not ('question' in body and 'answer' in body and 'category' in body and 'difficulty' in body):
            abort(422)

        question = Question(
            question=body.get('question'),
            answer=body.get('answer'),
            category=body.get('category'),
            difficulty=body.get('difficulty')
        )
        question.insert()

        return jsonify({
            'success': True,
            'created': question.id
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            if question is None:
                abort(404)

            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })

        except Exception as e:
            print(e)
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app