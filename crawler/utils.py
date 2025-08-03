import resend
from jinja2 import Environment, FileSystemLoader
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


RESEND_API_KEY = settings.get("RESEND_API_KEY")


def generate_mail(context):
    env = Environment(loader=FileSystemLoader(settings.get("TEMPLATES_DIR")))
    template = env.get_template("email.html")
    html = template.render(**context)

    return html


def send_mail(subject, receivers, body):
    params: resend.Emails.SendParams = {
        "from": settings.get("EMAIL_FROM"),
        "to": receivers,
        "subject": subject,
        "html": body,
    }

    email = resend.Emails.send(params)
