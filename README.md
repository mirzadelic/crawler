# Crawler
Scrapy crawler fetches ads from filtered URL of one of the websites and send an email with new and updated ads.

The crawler is sending `new` ads(ads that are fetched the first time for that site/URL), and `updated` ads(which are already fetched but the price changed so you can see previous and new price).

It uses the Postgres database to store ads and sites/URLs.

Available websites:
- polovniautomobili.com
- kupujemprodajem.com

## Instalation
Create virtualenv and install requirements:
```sh
pip install -r requirements.txt
```

Create a `crawler/.env` file. Use `crawler/.env.example` to see all possible variables.


## Usage

### Create site settings
Create a new site/URL with:
```sh
python create_site_url.py
```

### Run crawler
```sh
python run.py
```
This will run crawler and send an email with new and updated ads based on the last visit.


### Cronjob
You can set up a cronjob to run the command every couple of hours.

For example, this is my cronjob on server:
```sh
0 10,20 * * * cd /opt/crawler/crawler/ && ../venv/bin/python3 run.py
```
Will run every day at 10:00 and 20:00 to get email about new and updated ads.

## Info

This is made for personal usage.
Feel free to use it, add more spiders or improve code.


#### Contact

- E-mail: me@mirzadelic.com
- Website: www.mirzadelic.com
