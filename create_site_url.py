#!/usr/bin/python

import re
import sys

from crawler.db import session
from crawler.db.models import Site, create_tables
from run import SPIDERS_MAP

create_tables()


def validate_email(email):
    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(email_regex, email):
        sys.exit(f'Email address not valid: {email}.')
    return email


def main():
    print('--- Enter info ---')

    site = input("Site (polovniautomobili.com, kupujemprodajem.com): ")
    if site not in SPIDERS_MAP.keys():
        sys.exit('Entered site not available.')
    url = input("URL of first page to crawl: ")
    if site not in url:
        sys.exit('Entered URL not valid.')
    recipients = input("Recipients email (separated by comma for multi): ")
    recipients = [validate_email(r.strip()) for r in recipients.split(',')]
    name = input("Enter name/title of site settings(example: Ads for car): ")

    s = Site(name=name, site=site, url=url, recipients=recipients)
    session.add(s)
    session.commit()

    print(f'Site "{name}" added.')
    print('Run "python run.py" to run worker to get new ads.')


if __name__ == '__main__':
    main()
