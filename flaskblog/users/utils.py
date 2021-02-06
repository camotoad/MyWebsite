import os
from flask_mail import Message
from flask import url_for, current_app
from flaskblog import mail
from os import path

def save_picture(picture):

    picture_path = os.path.join(current_app.root_path, 'static/pics', picture.filename)
    if path.exists(picture_path):
        return None
    else:
        picture.save(picture_path)
        return picture.filename

def send_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', recipients=[user.email])
    msg.body = f'''Please click the link below to reset your password:
{url_for('users.reset_password', token=token, _external=True)}

If you did not make this request, you may ignore this email and no changes will be made.
'''
    mail.send(msg)
