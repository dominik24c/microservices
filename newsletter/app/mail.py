import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from . import config


def get_message(subject: str, content: str, receiver_email: str) -> MIMEMultipart:
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = 'Johnny Cash <johnnyc@gmail.com>'
    message["To"] = receiver_email

    text = f"""
        Hi!
        {content}
    """

    html = f"""
    <html>
    <body>
        <h3>Hi!</h3>
        <p>How are you?</p>
        <p>{content}</p>
    </body>
    </html>
    """

    text_part = MIMEText(text, "plain")
    html_part = MIMEText(html, "html")
    
    message.attach(text_part)
    message.attach(html_part)
    
    return message
    


def send_email(subject: str, content: str, receiver_email: str) -> None:
    with smtplib.SMTP(config.SMTP_SERVER, config.PORT) as server:
        message = get_message(subject, content, receiver_email)
        server.login(config.USERNAME, config.PASSWORD)
        server.sendmail(message["From"], message["To"], message.as_string())

