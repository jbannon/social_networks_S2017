import argparse
import json
import os
from hashlib import sha1
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from boilerpipe.extract import Extractor
from crawler.urls import URLS

@defer.inlineCallbacks
def crawl(runner):
    for url in URLS:
        yield runner.crawl("news", url=url)

    reactor.stop()

def start_crawl(args):
    configure_logging()

    settings = get_project_settings()
    settings.set('CLOSESPIDER_ITEMCOUNT', args.count)

    runner = CrawlerRunner(settings)

    crawl(runner)
    reactor.run()

def extract(args):
    if not os.path.isfile("articles.json"):
        print "File articles.json does not exist"
        print "Have you already crawled?"
        exit()

    with open("articles.json") as article_list:
        articles = [json.loads(line) for line in article_list.read().splitlines()]

    for article in articles:
        if args.html:
            with open(article['path'], "rb") as html:
                extractor = Extractor(extractor='ArticleExtractor', html=html.read())
        else:
            extractor = Extractor(extractor='ArticleExtractor', url=article['url'])

        dirname = os.path.join("articles", article['domain']) + "/text"
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        filename = sha1(article['url']).hexdigest() + '.txt'
        path = os.path.join(dirname, filename)

        with open(path, "wb+") as extracted_text:
            extracted_text.write(extractor.getText().encode("utf-8"))

def main():
    parser = argparse.ArgumentParser(description='Social Networks Spring 2017')
    parser.add_argument('method', choices=['crawl', 'extract'],
                        help='The functionality you wish to invoke')
    parser.add_argument('-c', '--count', type=int, default=10,
                        help='Number of items to limit crawl (Default: 10)')
    parser.add_argument('--html', action='store_true',
                        help="Extracts article text from html instead of urls (Default: false)")

    args = parser.parse_args()

    switcher = {
        'crawl': start_crawl,
        'extract': extract
    }

    func = switcher.get(args.method)
    func(args)

if __name__ == '__main__':
    main()
