from app import User, app
import requests
import jwt
from flask import render_template

    
def send_email(from_email, user, habit, action, start, end, token):
    email = jwt.decode(token, 'dankmemes', algorithms=['HS256'])['email']
    u = User.query.filter_by(email=email, id=user.id).first()
    if u == user:
        with app.app_context():
            html = render_template('email-premailer.html',
                                    user=u,
                                    habit=habit,
                                    action=action,
                                    start=start,
                                    end=end,
                                    token=token)
        data = {
            'from': 'Mailgun Sandbox <postmaster@sandboxd9f0d0d632064804af25ea31625cb4ea.mailgun.org>',
            'to': '{} {} <{}>'.format(u.first_name, u.last_name, u.email),
            'subject': 'Habiticci: {}'.format(habit.title),
            'html': html,
        }

        requests.post(
            "https://api.mailgun.net/v3/sandboxd9f0d0d632064804af25ea31625cb4ea.mailgun.org/messages",
            auth=("api", "key-6af38b5f7870b2b800c27bb9606712ed"),
            data=data)