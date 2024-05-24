import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urlparse
import re

class MenuSpider(CrawlSpider):
    name = 'menu_spider'
    
    def __init__(self, start_url, *args, **kwargs):
        super(MenuSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.allowed_domains = [urlparse(start_url).netloc]
        self.rules = (
            Rule(LinkExtractor(), callback='parse_item', follow=True),
        )
        super(MenuSpider, self)._compile_rules()
    
    def parse_item(self, response):
        menu_selectors = [
            '//a[contains(@href, "menu")]/@href',
            '//a[contains(@href, "menü")]/@href',
            '//a[contains(@href, "Menu")]/@href',
            '//a[contains(@href, "Menü")]/@href',
            '//a[contains(@href, "MENU")]/@href',
            '//a[contains(@href, "MENÜ")]/@href',
            '//a[contains(text(), "menu")]/@href',
            '//a[contains(text(), "menü")]/@href',
            '//a[contains(text(), "Menu")]/@href',
            '//a[contains(text(), "Menü")]/@href',
            '//a[contains(text(), "MENU")]/@href',
            '//a[contains(text(), "MENÜ")]/@href',
            '//img[contains(@src, "menu")]/@src',
            '//img[contains(@src, "menü")]/@src',
            '//img[contains(@src, "Menü")]/@src',
            '//img[contains(@src, "MENU")]/@src',
            '//img[contains(@src, "MENÜ")]/@src',
            '//a[contains(@href, ".pdf")]/@href'
        ]
        
        menu_urls = set()
        for selector in menu_selectors:
            menu_urls.update(response.xpath(selector).extract())
        
        for menu_url in menu_urls:
            menu_url = response.urljoin(menu_url)
            if menu_url.endswith('.pdf'):
                yield {'menu_pdf': menu_url}
            elif re.search(r'\.(jpg|jpeg|png)$', menu_url):
                yield {'menu_image': menu_url}
            else:
                yield scrapy.Request(menu_url, callback=self.parse_menu_text)
    
    def parse_menu_text(self, response):
        text_content = ' '.join(response.xpath('//text()').extract())
        if 'menu' in text_content.lower():
            yield {'menu_text': text_content.strip()}

# To run this spider:
# 1. Save the above code in a file named menu_spider.py inside the spiders directory of your Scrapy project.
# 2. Run the spider using the command: scrapy crawl menu_spider -a start_url=<restaurant_homepage_url>
