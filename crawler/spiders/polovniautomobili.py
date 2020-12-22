import scrapy
from crawler.db import session
from crawler.db.models import Site
from crawler.items import Item

from .base import BaseSpider


class PolovniautomobiliSpider(BaseSpider, scrapy.Spider):
    name = 'polovniautomobili'
    allowed_domains = ['polovniautomobili.com']
    base_url = 'https://www.polovniautomobili.com'
    start_urls = []
    site = None

    def __init__(self, site_id, **kwargs):
        super().__init__(**kwargs)
        self.site = session.query(Site).filter(Site.id == int(site_id)).one_or_none()
        if self.site:
            self.start_urls = [self.site.url]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        ads = set(
            response.css(
                'div#search-results [data-classifiedid]::attr(data-classifiedid)'
            ).getall()
        )

        for ad in ads:
            yield self.fetch_ad(ad)

        next_url = response.css('ul.uk-pagination li a[rel="next"]::attr(href)').get()
        if next_url:
            yield scrapy.Request(
                url=f'{self.base_url}{next_url}',
                callback=self.parse
            )

    def fetch_ad(self, ad_id):
        url = f'https://www.polovniautomobili.com/auto-oglasi/{ad_id}/ad'
        return scrapy.Request(url=url, callback=self.parse_ad, meta={'ad_id': ad_id})

    def parse_ad(self, response):
        content = response.css('div.uk-container.body')

        title = content.css('h1.h1-classified-title::text').get()
        image = content.css('ul#image-gallery li img::attr(src)').get()

        price = content.css('div.price-item-discount::text').extract()
        if price:
            price = next((p.strip() for p in price if p.strip()))
        else:
            price = content.css('div.price-item::text').get().strip()

        item = Item()
        item['site'] = self.site
        item['source_id'] = response.meta['ad_id']
        item['url'] = response.url
        item['title'] = title
        item['price'] = price
        item['image'] = image

        return item
