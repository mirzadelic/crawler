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
            # Add headers to mimic a real browser
            yield Request(url, callback=self.parse, errback=self.handle_error)
            # headers = {
            #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            #     "Accept-Language": "en-US,en;q=0.5",
            #     "Accept-Encoding": "gzip, deflate",
            #     "Connection": "keep-alive",
            #     "Upgrade-Insecure-Requests": "1",
            #     "Sec-Fetch-Dest": "document",
            #     "Sec-Fetch-Mode": "navigate",
            #     "Sec-Fetch-Site": "none",
            #     "Cache-Control": "max-age=0",
            #     "DNT": "1",
            #     "Sec-GPC": "1",
            # }
            # yield Request(
            #     url,
            #     headers=headers,
            #     callback=self.parse,
            #     errback=self.handle_error,
            #     meta={"handle_httpstatus_list": [403]},  # Don't treat 403 as error
            # )

    def handle_error(self, failure):
        print(f"Request failed: {failure.request.url}")
        print(f"Error: {failure.value}")
        print(f"Error type: {failure.type}")

        # Check if failure has a response (HTTP errors like 404, 500, etc.)
        if failure.check(HttpError):
            response = failure.value.response
            print(f"HTTP Error - Status code: {response.status}")
            print(f"Response headers: {response.headers}")

            # Decode response body for better readability
            try:
                body_text = response.body.decode("utf-8")
                print(f"Response body (first 1000 chars): {body_text[:1000]}")

                # Check if it's a Cloudflare block page
                if "cloudflare" in body_text.lower() and "blocked" in body_text.lower():
                    print("⚠️  DETECTED: Cloudflare is blocking this request")
                    print("Consider using:")
                    print("- Rotating user agents")
                    print("- Adding delays between requests")
                    print("- Using scrapy-splash or selenium")
                    print("- Implementing CAPTCHA solving")

            except UnicodeDecodeError:
                print(f"Response body (raw bytes, first 500): {response.body[:500]}")

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
