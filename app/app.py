from flask import Flask, send_from_directory, current_app
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse


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
        return u

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str)
        parser.add_argument('last_name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        print args
        print args['first_name'], args['last_name'], args['email'], args['password']
        u = User(args['first_name'], args['last_name'], args['email'], args['password'])
        print u
        if u:
            db.session.add(u)
            db.session.commit()


api.add_resource(Login, '/login')


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
        self.password = password

    def __repr__(self):
        return '<User {}>'.format(self.email)


@app.route("/")
def main():
    return send_from_directory(current_app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True)
