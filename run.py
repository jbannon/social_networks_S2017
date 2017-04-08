import argparse
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
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

def main():
    parser = argparse.ArgumentParser(description='Social Networks Spring 2017')
    parser.add_argument('method', choices=['crawl'], help='The functionality you wish to invoke')
    parser.add_argument('-c', '--count', type=int, default=10,
                        help='Number of items to limit crawl (Default: 10)')

    args = parser.parse_args()

    switcher = {
        'crawl': start_crawl
    }

    func = switcher.get(args.method)
    func(args)

if __name__ == '__main__':
    main()
