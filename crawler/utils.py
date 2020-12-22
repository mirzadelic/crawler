import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, FileSystemLoader
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


def generate_mail(context):
    env = Environment(loader=FileSystemLoader(settings.get('TEMPLATES_DIR')))
    template = env.get_template("email.html")
    html = template.render(**context)

    return html


def send_mail(subject, receivers, body):
    SMTP_SERVER = settings.get('SMTP_SERVER')
    SMTP_PORT = settings.get('SMTP_PORT')
    SMTP_USERNAME = settings.get('SMTP_USERNAME')
    SMTP_PASSWORD = settings.get('SMTP_PASSWORD')

    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = SMTP_USERNAME
    message['To'] = ', '.join(receivers)
    html_body = MIMEText(body, 'html')
    message.attach(html_body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, receivers, message.as_string())
