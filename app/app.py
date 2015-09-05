from flask import Flask, send_from_directory, current_app
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
api = Api(app)

class Login(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        u = User.query.filter_by(email=args['email']).first()
        if not u:
            return {'error': 'User not found.'}
        if u.check_password(args['password']):
            return {'token': jwt.encode({'email': args['email']}, 'dankmemes', algorithm='HS256')}
        else:
            return {'error': 'Incorrect password specified.'}


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


class UserRoute(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str)
        args = parser.parse_args()
        email = jwt.decode(args['token'], 'dankmemes', algorithms=['HS256'])['email']
        u = User.query.filter_by(email=email).first()
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
            return {'email': u.email,
                    'first_name': u.first_name,
                    'last_name': u.last_name,
                    'habits': habits
                    }


class HabitRoute(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str)
        parser.add_argument('token', type=str)
        parser.add_argument('token', type=str)
        args = parser.parse_args()
        email = jwt.decode(args['token'], 'dankmemes', algorithms=['HS256'])['email']
        u = User.query.filter_by(email=email).first()
        if not u:
            return {'error': 'User not found.'}
        else:
            return {'email': u.email,
                    'first_name': u.first_name,
                    'last_name': u.last_name}


api.add_resource(Login, '/login')
api.add_resource(UserRoute, '/user')
api.add_resource(HabitRoute, '/habit')


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
    # 0 = minute, 1 = hour, 2 = day, 3 = week, 4 = month, 5 = year
    frequency_type = db.Column(db.Integer)

    def __init__(self, user_id, title, description, frequency, frequency_type):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.frequency = frequency
        self.frequency_type = frequency_type

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

    def __init__(self, habit_id, user_id):
        self.habit_id = habit_id
        self.user_id = user_id
        self.sent = datetime.now() 

    def __repr__(self):
        return '<Action #{} for Habit #{}>'.format(self.id, self.habit_id)


@app.route("/")
def main():
    return send_from_directory(current_app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True)
