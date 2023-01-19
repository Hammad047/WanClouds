import smtplib
from email.message import EmailMessage
from authentication.consts import *

# from authentication.consts


def send_email(self, email_receiver):
    """
    This function is used to send email to the user when he/she sign up on this app. SMTP server is used for
    this purpose.
    :return:
    """

    email_obj = EmailMessage()
    email_obj['Subject'] = subject
    email_obj['From'] = email_sender
    email_obj['To'] = email_receiver
    email_obj.set_content(body)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_sender, email_sender_password)
    server.sendmail(email_sender, email_receiver, email_obj.as_string(()))
