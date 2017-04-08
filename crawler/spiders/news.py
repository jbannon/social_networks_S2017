from urlparse import urljoin, urlparse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawler.items import Article
import crawler.rules as rules

class NewsSpider(CrawlSpider):
    name = 'news'

    DEPTH_PRIORITY = 1

    def __init__(self, url, *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)

        domain = urlparse(url).netloc
        self.allowed_domains = [domain]
        self.start_urls = [url]

        allow = [urljoin(url, regex) for regex in rules.ALLOW]
        deny = [urljoin(url, regex) for regex in rules.DENY]

        NewsSpider.rules = (
            Rule(LinkExtractor(allow=allow, deny=deny), callback='parse_item', follow=True),
            Rule(LinkExtractor(allow=url)),
        )
        super(NewsSpider, self)._compile_rules()

    def parse_item(self, response):
        article = Article()

        article['url'] = response.url
        article['title'] = response.css('title::text').extract_first()
        article['html'] = response.body

        yield article
