from app import User
import requests
import jwt
from flask import render_template

    
def send_email(from_email, user, habit, start, end, token):
    email = jwt.decode(args['token'], 'dankmemes', algorithms=['HS256'])['email']
    u = User.query.filter_by(email=email, id=user_id).first()
    if u == user:
        html = render_template('email-premailer.html',
                                user=u,
                                habit=habit,
                                start=start,
                                end=end,
                                token=token)
        data = {
            'from': 'Mailgun Sandbox <postmaster@sandboxd53a543015474b0f8084fa6402db6e42.mailgun.org>',
            'to': '{} {} <{}>'.format(u.first_name, u.last_name, u.email),
            'subject': 'Habiticci: {}'.format(habit.title),
            'html': html,
        }

        requests.post(
            "https://api.mailgun.net/v3/sandboxd53a543015474b0f8084fa6402db6e42.mailgun.org/messages",
            auth=("api", "key-531afc342026055aad026d20264e956f"),
            data=data)