from urllib.parse import parse_qsl, urlencode, urlparse

from crawler.items import Item
from scrapy import Request, Selector

from .base import BaseSpider


class NekretnineSpider(BaseSpider):
    name = 'nekretnine'
    allowed_domains = ['nekretnine.rs']
    base_url = 'https://www.nekretnine.rs'

    def parse(self, response):
        ads = response.css(
            'div.offer-container div.offer'
        ).getall()
        for ad_html in ads:
            yield self.parse_ad(ad_html)

        next_url = self.get_next_url(response)
        if next_url:
            yield Request(url=next_url, callback=self.parse)

    def get_next_url(self, response):
        next_url = response.css('div.page-numbers a.next-article-button::attr(href)').get()
        if next_url:
           return f'{self.base_url}{next_url}'

        return None

    def parse_ad(self, ad_html):
        selector = Selector(text=ad_html)
        title_elem = selector.css('.offer-title a')
        title = title_elem.css('::text').get().strip()
        url = title_elem.css('::attr(href)').get().strip()
        url = f'{self.base_url}{url}'
        source_id = url.rsplit('/', 2)[1]
        image = selector.css('picture.advert-picture img::attr(data-src)').get().strip()
        price = selector.css('p.offer-price span::text').get().strip()

        item = Item()
        item['site'] = self.site
        item['source_id'] = source_id
        item['url'] = url
        item['title'] = title
        item['price'] = price
        item['image'] = image

        return item
