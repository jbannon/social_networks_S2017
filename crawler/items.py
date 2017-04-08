import scrapy

class Article(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    html = scrapy.Field()
    path = scrapy.Field()

    def __repr__(self):
        return repr({"title": self['title']})
