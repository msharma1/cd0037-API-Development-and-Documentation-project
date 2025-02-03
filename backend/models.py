from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def setup_db(app, database_path="postgresql://localhost:5432/trivia"):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }