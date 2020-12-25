from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from crawler.db import session
from crawler.db.models import Site, create_tables
from crawler.spiders.kupujemprodajem import KupujemprodajemSpider
from crawler.spiders.nekretnine import NekretnineSpider
from crawler.spiders.polovniautomobili import PolovniautomobiliSpider

create_tables()

SPIDERS_MAP = {
    'polovniautomobili.com': PolovniautomobiliSpider,
    'kupujemprodajem.com': KupujemprodajemSpider,
    'nekretnine.rs': NekretnineSpider
}


def main():
    process = CrawlerProcess(get_project_settings())

    sites = session.query(Site).filter(Site.active.is_(True))
    if sites.count() == 0:
        print(
            'No site urls added. '
            'Use "python create_site_url.py" command to add url.'
        )
    for site in sites:
        process.crawl(SPIDERS_MAP[site.site], site_id=site.id)

    process.start()


if __name__ == '__main__':
    main()
