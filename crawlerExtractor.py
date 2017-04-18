from newspaper import Article
from boilerpipe.extract import Extractor
import urllib2, requests
import io, json
from bs4 import BeautifulSoup, SoupStrainer
from timeout import timeout

hdr = { 'User-Agent' : 'super friendly bot' }
MIN_ARTICLE_LENGTH = 500
MAX_ARTICLES = 50

def getRelatedURLs(url):
	relatedURLs = []
	# try:
	# 	response = requests.get(url)
	# 	html = response.content
	# except:
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	req = urllib2.Request(url, headers=hdr)
	html = opener.open(req)
	for link in BeautifulSoup(html, parse_only=SoupStrainer("a", href=True)).find_all("a"):
		relatedURLs.append(link['href'])
	return relatedURLs

@timeout(10)
def getContentFromNewspaper(url):
	content, title, authors, date = (u'', )*4
	article = Article(url)
	article.download()
	article.parse()
	content = article.text
	title = article.title
	authors = article.authors
	date = article.publish_date
	return content, title, authors, date

@timeout(10)
def getContentFromBoilerpipe(url):
	content = u''
	extractor = Extractor(extractor='ArticleExtractor', url = url)
	content = extractor.getText()
	return content

def getContent(url):
	content, title, authors, date = (u'', )*4
	try:
		content, authors, title = getContentFromNewspaper(url)
	except:
		try:
			content = getContentFromBoilerpipe(url)
		except:
			pass
	return content, title, authors, date

def isPotentialArticle(url):
	if (url[-1] != "/") and (url.count('-') > 4) \
						and not any(exclude in url for exclude in nonArticles):
		return True
	else:
		return False

listlinks = []
main = "http://www.npr.org"
toVisit = [main]
toVisitandVisited = toVisit
nonArticles = ["video", "facebook", "twitter", "digg", "pinterest", "mailto", "linkedin", "#"]
relatedURLs = []

with io.open('articles.txt', 'w', encoding="utf-8") as output:
	if (main[-1] == "/"):	# for concatenation of sublinks which start with "/"
		main = main[:-1]
	while(len(listlinks) < MAX_ARTICLES and len(toVisit) > 0):
		url = toVisit[0]
		toVisit = toVisit[1:]
		content, title, authors, date = getContent(url)

		if (url == main) or (url != main and len(content) > MIN_ARTICLE_LENGTH):
			if len(content) > MIN_ARTICLE_LENGTH:
				data = {"url" : url, "title" : title, "date" : date, "authors" : authors, "content" : content}
				output.write(json.dumps(data, ensure_ascii=False))
				output.write(u'\n')
				listlinks.append(url)

			relatedURLs = getRelatedURLs(url)
			for relatedURL in relatedURLs:
				if (isPotentialArticle(relatedURL)):
					if relatedURL[0] == "/":
						relatedURL = main + relatedURL
					if main[5:] in relatedURL:						# if https links fetched but main is http
						if relatedURL not in toVisitandVisited:
							toVisit.append(relatedURL)
							toVisitandVisited.append(relatedURL)


