from crawler.db import session
from crawler.db.models import Site
from scrapy import Request, Spider
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import (
    DNSLookupError,
    TimeoutError,
    TCPTimedOutError,
    ConnectionRefusedError,
)


class BaseSpider(Spider):
    start_urls = []
    site = None

    def __init__(self, site_id, **kwargs):
        self.site = session.query(Site).filter(Site.id == site_id).one_or_none()
        if self.site:
            self.start_urls = [self.site.url]

    def start_requests(self):
        for url in self.start_urls:
            print(url)
            yield Request(url, callback=self.parse, errback=self.handle_error)

    def handle_error(self, failure):
        print(f"Request failed: {failure.request.url}")
        print(f"Error: {failure.value}")
        print(f"Error type: {failure.type}")

        # Check if failure has a response (HTTP errors like 404, 500, etc.)
        if failure.check(HttpError):
            response = failure.value.response
            print(f"HTTP Error - Status code: {response.status}")
            print(f"Response headers: {response.headers}")
            print(f"Response body: {response.body}")  # First 500 chars

        # Check for DNS lookup failures
        elif failure.check(DNSLookupError):
            print(f"DNS Lookup failed for: {failure.request.url}")

        # Check for timeout errors
        elif failure.check(TimeoutError, TCPTimedOutError):
            print(f"Request timed out for: {failure.request.url}")

        # Check for connection refused
        elif failure.check(ConnectionRefusedError):
            print(f"Connection refused for: {failure.request.url}")

    def get_next_url(self, response):
        raise NotImplemented
