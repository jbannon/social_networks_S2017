import json
import os
from hashlib import sha1
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonLinesItemExporter

class CrawlerPipeline(object):
    def __init__(self):
        self.file = None
        self.exporter = None
        self.dirname = None
        self.articles_seen = set()

    def open_spider(self, spider):
        self.file = open('articles.json', 'a+b')

        self.exporter = JsonLinesItemExporter(self.file)
        self.exporter.start_exporting()

        self.file.seek(0)
        articles_seen = [json.loads(line)['url'] for line in self.file.read().splitlines()]
        self.articles_seen = set(articles_seen)

        self.dirname = os.path.join("articles", spider.allowed_domains[0]) + "/html"
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, article, spider):
        if article['url'] in self.articles_seen:
            raise DropItem("Duplicate article found: %s" % article)

        filename = sha1(article['url']).hexdigest() + '.html'
        path = os.path.join(self.dirname, filename)

        item = {
            "domain": spider.allowed_domains[0],
            "url": article['url'],
            "title": article['title'],
            "path": path
        }

        with open(path, 'wb+') as f:
            f.write(article['html'])

        self.exporter.export_item(item)
        self.articles_seen.add(article['url'])

        return article
