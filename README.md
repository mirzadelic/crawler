# Crawler
Scrapy crawler to fetch car ads from filtered URL of polovniautomobili.com and send an email with new and updated car ads.

The crawler is sending `new` items(items that are fetched the first time for that site/URL), and `updated` items(which are already fetched but the price changed so you can see previous and new price).

It uses the Postgres database to store items and sites/URLs.

Available websites:
- polovniautomobili.com

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
This will run crawler and send an email with new and updated items based on the last visit.


You can set up a cronjob to run the command every couple of hours.


## Info

This is made for personal usage.
Feel free to use it, add more spiders or improve code.


#### Contact

- E-mail: me@mirzadelic.com
- Website: www.mirzadelic.com
