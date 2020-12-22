from .db import session
from .db.models import Ad
from .utils import generate_mail, send_mail


class CrawlerPipeline:

    def __init__(self):
        self.updated_ads = []
        self.new_ads = []

    def open_spider(self, spider):
        print(f'Opening spider: {spider.site}')

    def close_spider(self, spider):
        print(f'Closing spider: {spider.site}')
        if self.new_ads or self.updated_ads:
            print(
                f'Sending {len(self.new_ads)} new and ' \
                f'{len(self.updated_ads)} updated ads to: {spider.site.recipients}.'
            )
            site = spider.site
            body = generate_mail({
                'new_ads': self.new_ads,
                'updated_ads': self.updated_ads,
                'site': site
            })
            send_mail(f'Ads for: {site.name}', site.recipients, body)

        print(f'Closed spider: {spider.site}')

    def process_item(self, item, spider):

        current_item = session.query(Ad).filter(
            Ad.source_id == item['source_id'],
            Ad.site_id == spider.site.id
        ).one_or_none()

        if current_item:
            item_price = item['price']
            if not current_item.price or (
                current_item.price and current_item.price[0] != item_price
            ):
                current_item.price = [item_price] + current_item.price
                session.commit()
                self.updated_ads.append(current_item)
        else:
            ad = Ad(
                site_id=item['site'].id,
                source_id=item['source_id'],
                url=item['url'],
                title=item['title'],
                price=[item['price']] if item['price'] else [],
                image=item['image']
            )
            session.add(ad)
            session.commit()
            self.new_ads.append(ad)

        return item
