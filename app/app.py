from flask import Flask, send_from_directory, current_app, abort
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
api = Api(app)

class LoginAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        u = User.query.filter_by(email=args['email']).first()
        if not u:
            return abort(401)
            # return {'error': 'User not found.'}
        if u.check_password(args['password']):
            return {'token': jwt.encode({'email': args['email'], 'id': u.id}, 'dankmemes', algorithm='HS256')}
        else:
            return abort(401)
            # return {'error': 'Incorrect password specified.'}


class CreateUserAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str)
        parser.add_argument('last_name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        u = User(args['first_name'], args['last_name'], args['email'], args['password'])
        if u:
            db.session.add(u)
            db.session.commit()
            return {'token': jwt.encode({'email': args['email'], 'id': u.id}, 'dankmemes', algorithm='HS256')}
        else:
            return {'error': 'User could not be created.'}


class UserAPI(Resource):
    def get(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str)
        args = parser.parse_args()
        email = jwt.decode(args['token'], 'dankmemes', algorithms=['HS256'])['email']
        u = User.query.filter_by(email=email, id=id).first()
        if not u:
            return {'error': 'User not found.'}
        else:
            actions = []
            for action in u.actions:
                actions.append({'id': action.id,
                                'sent': action.sent,
                                'received': action.received,
                                'answer': action.answer})
            return {'user_id': u.id,
                    'email': u.email,
                    'first_name': u.first_name,
                    'last_name': u.last_name,
                    'actions': actions
                   }

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str)
        parser.add_argument('last_name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        email = jwt.decode(args['token'], 'dankmemes', algorithms=['HS256'])['email']
        u = User.query.filter_by(email=email, id=id).first()
        if not u:
            return {'error': 'User not found.'}
        for k, v in args.items():
            if v is not None:
                setattr(u, k, v)
        db.session.commit()

    def delete(self, id):
        email = jwt.decode(args['token'], 'dankmemes', algorithms=['HS256'])['email']
        u = User.query.filter_by(email=email, id=id).first()
        if not u:
            return {'error': 'User not found.'}
        db.session.delete(u)
        db.session.commit()


class AllHabitsAPI(Resource):
    def get(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str)
        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('frequency', type=int)
        parser.add_argument('frequency_type', type=int)
        args = parser.parse_args()
        email = jwt.decode(args['token'], 'dankmemes', algorithms=['HS256'])['email']
        u = User.query.filter_by(email=email, id=user_id).first()
        if not u:
            return {'error': 'User not found.'}
        else:
            habits = []
            for habit in u.habits:
                habits.append({'id': habit.id,
                               'title': habit.title,
                               'description': habit.description,
                               'frequency': habit.frequency,
                               'frequency_type': habit.frequency_type})
            return {'habits': habits}


    def post(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str)
        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('frequency', type=int)
        args = parser.parse_args()
        email = jwt.decode(args['token'], 'dankmemes', algorithms=['HS256'])['email']
        u = User.query.filter_by(email=email, id=user_id).first()
        if not u:
            return {'error': 'User not found.'}
        else:
            habit = Habit(user=u,
                          title=args['title'],
                          description=args.get('description'),
                          frequency=args['frequency'])
            if habit:
                db.session.add(habit)
                db.session.commit()
                return {'id': habit.id,
                        'title': habit.title,
                        'description': habit.description,
                        'frequency': habit.frequency,
                        'frequency_type': habit.frequency_type}
            else:
                return {'error': 'Habit could not be created.'}


class HabitAPI(Resource):
    def get(self, user_id, habit_id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str)
        args = parser.parse_args()
        email = jwt.decode(args['token'], 'dankmemes', algorithms=['HS256'])['email']
        u = User.query.filter_by(email=email, id=user_id).first()
        if not u:
            return {'error': 'User not found.'}
        else:
            habit = Habit.query.filter_by(user_id=user_id, id=habit_id).first()
            if not habit:
                return {'error': 'Habit not found.'}
            else:
                actions = []
                for action in habit.actions:
                    actions.append({'id': action.id,
                                    'sent': action.sent,
                                    'received': action.received,
                                    'answer': action.answer})
                return {'id': habit.id,
                        'title': habit.title,
                        'description': habit.description,
                        'frequency': habit.frequency,
                        'frequency_type': habit.frequency_type,
                        'actions': actions}

    def put(self, user_id, habit_id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str)
        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('frequency', type=int)
        parser.add_argument('frequency_type', type=int)
        args = parser.parse_args()
        email = jwt.decode(args['token'], 'dankmemes', algorithms=['HS256'])['email']
        u = User.query.filter_by(email=email, id=user_id).first()
        if not u:
            return {'error': 'User not found.'}
        habit = Habit.query.filter_by(user_id=user_id, id=habit_id).first()
        if not habit:
            return {'error': 'Habit not found.'}
        for k, v in args.items():
            if v is not None:
                setattr(habit, k, v)
        db.session.commit()

    def delete(self, user_id, habit_id):
        email = jwt.decode(args['token'], 'dankmemes', algorithms=['HS256'])['email']
        u = User.query.filter_by(email=email, id=user_id).first()
        if not u:
            return {'error': 'User not found.'}
        habit = Habit.query.filter_by(user_id=user_id, id=habit_id).first()
        if not habit:
            return {'error': 'Habit not found.'}
        db.session.delete(habit)
        db.session.commit()


class ActionAPI(Resource):
    def get(self, user_id, habit_id, action_id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str)
        parser.add_argument('answer', type=str)
        args = parser.parse_args()
        email = jwt.decode(args['token'], 'dankmemes', algorithms=['HS256'])['email']
        u = User.query.filter_by(email=email, id=user_id).first()
        action = Action.query.filter_by(id=action_id,
                                        user=u,
                                        habit_id=habit_id).first()
        print action, action.received
        if not action.received:
            print datetime.now()
            print args['answer']
            action.received = datetime.now()
            action.answer = args['answer']
            action.save()
        db.session.commit()
        return send_from_directory(current_app.static_folder, "index.html")


api.add_resource(LoginAPI, '/token')
api.add_resource(CreateUserAPI, '/user')
api.add_resource(UserAPI, '/user/<int:id>')
api.add_resource(AllHabitsAPI, '/user/<int:user_id>/habits')
api.add_resource(HabitAPI, '/user/<int:user_id>/habits/<int:habit_id>')
api.add_resource(ActionAPI, '/user/<int:user_id>/habits/<int:habit_id>/action/<int:action_id>')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)


class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
        backref=db.backref('habits', lazy='dynamic'))
    title = db.Column(db.String(140))
    description = db.Column(db.Text)
    frequency = db.Column(db.Integer)
    start = db.Column(db.DateTime)

    def __init__(self, user, title, description, frequency, start):
        self.user = user
        self.title = title
        self.description = description
        self.frequency = frequency
        self.start = datetime.now()

    def __repr__(self):
        return '<Habit #{} for User {}>'.format(self.id, self.user_id)


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'))
    habit = db.relationship('Habit',
        backref=db.backref('actions', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
        backref=db.backref('actions', lazy='dynamic'))
    sent = db.Column(db.DateTime)
    received = db.Column(db.DateTime)
    # 0 = Yes
    # 1 = Maybe
    # 2 = No
    answer = db.Column(db.Integer)

    def __init__(self, habit, user):
        self.habit = habit
        self.user = user
        self.sent = datetime.now()

    def __repr__(self):
        return '<Action #{} for Habit #{}>'.format(self.id, self.habit_id)


@app.route("/")
def main():
    return send_from_directory(current_app.static_folder, "index.html")


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == "__main__":
    app.run(debug=True)
