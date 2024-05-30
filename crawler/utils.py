from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import From, To, Subject, HtmlContent, Mail
import urllib.request as urllib
from jinja2 import Environment, FileSystemLoader
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


def generate_mail(context):
    env = Environment(loader=FileSystemLoader(settings.get("TEMPLATES_DIR")))
    template = env.get_template("email.html")
    html = template.render(**context)

    return html


def send_mail(subject, receivers, body):
    EMAIL_FROM = settings.get("EMAIL_FROM")
    SENDGRID_API_KEY = settings.get("SENDGRID_API_KEY")

    sendgrid_client = SendGridAPIClient(api_key=SENDGRID_API_KEY)
    from_email = From(EMAIL_FROM)
    to_emails = [To(receiver) for receiver in receivers]
    subject = Subject(subject)
    html_content = HtmlContent(body)

    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        plain_text_content=None,
        html_content=html_content,
    )

    try:
        sendgrid_client.send(message=message)
    except urllib.HTTPError as e:
        print(e.read())
        exit()
