from scrapy import Request

from crawler.items import Item

from .base import BaseSpider


class PolovniautomobiliSpider(BaseSpider):
    name = 'polovniautomobili'
    allowed_domains = ['polovniautomobili.com']
    base_url = 'https://www.polovniautomobili.com'

    def parse(self, response):
        ads = set(
            response.css(
                'div#search-results [data-classifiedid]::attr(data-classifiedid)'
            ).getall()
        )

        for ad in ads:
            yield self.fetch_ad(ad)

        next_url = self.get_next_url(response)
        if next_url:
            yield Request(
                url=next_url,
                callback=self.parse
            )

    def get_next_url(self, response):
        next_url = response.css(
            'ul.uk-pagination li a[rel="next"]::attr(href)').get()
        if next_url:
            return f'{self.base_url}{next_url}'

    def fetch_ad(self, ad_id):
        url = f'https://www.polovniautomobili.com/auto-oglasi/{ad_id}/ad'
        return Request(
            url=url,
            callback=self.parse_ad, meta={'ad_id': ad_id}
        )

    def parse_ad(self, response):
        content = response.css('div.uk-container.body')
        title = content.css('div.table-cell-left > h1::text').get().strip()
        image = content.css('ul#image-gallery li img::attr(src)').get().strip()

        # old way
        # price = content.css('div.price-item-discount::text').extract()
        # if price:
        #     price = next((p.strip() for p in price if p.strip()))
        # else:
        #     price = content.css('div.price-item::text').get().strip()

        # new way
        price = content.css('span.priceClassified::text').get().strip()

        item = Item()
        item['site'] = self.site
        item['source_id'] = response.meta['ad_id']
        item['url'] = response.url
        item['title'] = title
        item['price'] = price
        item['image'] = image

        return item
