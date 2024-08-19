from flask_mail import Mail, Message
from flask import render_template, url_for
from itsdangerous import URLSafeSerializer
from dotenv import load_dotenv
import os


load_dotenv()

mail = Mail()

# *Функція не повертатиме нічого*
def send_confirmation_mail(user_email) -> None:
    serializer = URLSafeSerializer(os.getenv('SECRET_KEY'))
    confirm_url = url_for(
        'confirm_email',
        token=serializer.dumps(user_email, salt='email-confirmation-salt'),
        _external=True
    )

    html = render_template('email_confirmation.html', confirm_url=confirm_url)
    message = Message(
        'Confirm Email Adress',
        recipients=[user_email],
        sender=('Flask Shop 21 Group', os.getenv('EMAIL')),
        html=html
    )
    mail.send(message=message)