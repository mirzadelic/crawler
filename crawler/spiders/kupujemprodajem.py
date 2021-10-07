from urllib.parse import parse_qsl, urlencode, urlparse

from crawler.items import Item
from scrapy import Request, Selector

from .base import BaseSpider


class KupujemprodajemSpider(BaseSpider):
    name = "kupujemprodajem"
    allowed_domains = ["kupujemprodajem.com"]
    base_url = "https://www.kupujemprodajem.com"

    def parse(self, response):
        ads = response.css("#adListContainer div.item:not(.head)").getall()

        for ad_html in ads:
            yield self.parse_ad(ad_html)

        next_url = self.get_next_url(response)
        if next_url:
            yield Request(url=next_url, callback=self.parse)

    def get_next_url(self, response):
        next_page = response.xpath(
            "//div[contains(@class, 'pageBarHolder')][1]/ul[contains(@class, 'pagesList')]/li[contains(@class, 'this-page')]/following-sibling::li[1]/a/text()"
        ).extract()
        next_page = next_page[0] if next_page else None
        if next_page:
            url = response.url
            url_parsed = urlparse(url)
            url_params = dict(parse_qsl(url_parsed.query))
            url_params["data[page]"] = next_page
            url_without_params = url_parsed.geturl().split("?")[0]
            url = f"{url_without_params}?{urlencode(url_params)}"

            return url

        return None

    def parse_ad(self, ad_html):
        selector = Selector(text=ad_html)
        source_id = selector.css("div.ad-options::attr(ad-id)").get()
        title_elem = selector.css("a.adName")
        title = title_elem.css("::text").get().strip()
        price = selector.css("span.adPrice::text").get().strip()
        url = title_elem.css("::attr(href)").get().strip()
        url = f"{self.base_url}{url}"
        image = selector.css("div.adImgWrapper img::attr(src)").get().strip()
        image = f"https:{image}"

        item = Item()
        item["site"] = self.site
        item["source_id"] = source_id
        item["url"] = url
        item["title"] = title
        item["price"] = price
        item["image"] = image

        return item
