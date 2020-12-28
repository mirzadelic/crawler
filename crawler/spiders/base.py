from crawler.db import session
from crawler.db.models import Site
from scrapy import Request, Spider


class BaseSpider(Spider):
    start_urls = []
    site = None

    def __init__(self, site_id, **kwargs):
        self.site = session.query(Site).filter(Site.id == site_id).one_or_none()
        if self.site:
            self.start_urls = [self.site.url]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def get_next_url(self, response):
        raise NotImplemented
