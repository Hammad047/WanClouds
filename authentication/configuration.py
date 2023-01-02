import smtplib
from email.message import EmailMessage
import jwt
import datetime
from app import app, db
from functools import wraps
from flask import  request
import jsonify

app.config['SECRET_KEY'] = 'WANCLOUDS-APP'

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'token is invalid'})
        return f(*args, **kwargs)
    return decorator

def send_email(self, email_receiver):
    email_sender =  '' #enter your email
    email_sender_password = '' #enter your password (app-password)
    subject = 'Email Verification'
    body = "Thank you for signing up on WanClouds App"
    email_obj = EmailMessage()
    email_obj['Subject'] = subject
    email_obj['From'] = email_sender
    email_obj['To'] = email_receiver
    email_obj.set_content(body)
    server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
    server.starttls()
    server.login(email_sender, email_sender_password)
    server.sendmail(email_sender, email_receiver, email_obj.as_string(()))