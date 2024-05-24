import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urlparse
import re


class MenuSpider(CrawlSpider):
    name = "menu_spider"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "ROBOTSTXT_OBEY": False,
    }

    def __init__(self, start_url, *args, **kwargs):
        super(MenuSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.allowed_domains = [urlparse(start_url).netloc]
        self.rules = (Rule(LinkExtractor(), callback="parse_item", follow=True),)
        super(MenuSpider, self)._compile_rules()

        self.keywords = [
            "menu",
            "menü",
            "Menu",
            "Menü",
            "MENU",
            "MENÜ",
            "karte",
            "Karte",
            "KARTE",
            "speise",
            "Speise",
            "SPEISE",
        ]

        self.visited_urls = set()

        # flag to track if any PDF or image has been found
        self.found_media = False

    def parse_item(self, response):
        menu_urls = set()

        for keyword in self.keywords:
            menu_urls.update(
                response.xpath(f'//a[contains(@href, "{keyword}")]/@href').extract()
            )
            menu_urls.update(
                response.xpath(f'//a[contains(text(), "{keyword}")]/@href').extract()
            )
            menu_urls.update(
                response.xpath(f'//img[contains(@src, "{keyword}")]/@src').extract()
            )

        menu_urls.update(response.xpath('//a[contains(@href, ".pdf")]/@href').extract())

        if menu_urls:

            # sort URLs so that PDFs and images are at the front of the list
            menu_urls = sorted(
                menu_urls.copy(),
                key=lambda x: x.endswith(".pdf")
                or bool(re.search(r"\.(jpg|jpeg|png)$", x)),
                reverse=True,
            )

            for menu_url in menu_urls:
                menu_url = response.urljoin(menu_url)
                if menu_url not in self.visited_urls:
                    self.visited_urls.add(menu_url)
                    if menu_url.endswith(".pdf"):
                        self.found_media = True
                        yield {"menu_pdf": menu_url}
                    elif re.search(r"\.(jpg|jpeg|png|gif|bmp|tiff)$", menu_url):
                        self.found_media = True
                        yield {"menu_image": menu_url}
                    else:
                        yield scrapy.Request(menu_url, callback=self.parse_menu_text)
        else:
            # check for embedded menu content only if no media has been found yet
            if not self.found_media:
                text_content = " ".join(response.xpath("//text()").extract())
                if any(
                    keyword.lower() in text_content.lower() for keyword in self.keywords
                ):
                    yield {"menu_text": text_content.strip()}

    def parse_menu_text(self, response):
        # check for embedded menu content only if no media has been found yet
        if not self.found_media:
            text_content = " ".join(response.xpath("//text()").extract())
            if "menu" in text_content.lower() and response.url not in self.visited_urls:
                self.visited_urls.add(response.url)
                yield {"menu_text": text_content.strip()}


# To run this spider:
# 1. Save the above code in a file named menu_spider.py inside the spiders directory of your Scrapy project.
# 2. Run the spider using the command: scrapy crawl menu_spider -a start_url=<restaurant_homepage_url> -O output.json
