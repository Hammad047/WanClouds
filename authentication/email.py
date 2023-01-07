import smtplib
from authentication import *

def send_email(self, email_receiver):
    email_sender = 'hammadkhanniazi420@yahoo.com'  # enter your email
    email_sender_password = 'rdhgdzlwxnkwyqrv'  # enter your password (app-password)
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
