from newspaper import Article
from boilerpipe.extract import Extractor
import urllib2, requests
import io, json
from bs4 import BeautifulSoup, SoupStrainer
from timeout import timeout

hdr = { 'User-Agent' : 'super friendly bot' }
MIN_ARTICLE_LENGTH = 500
MAX_ARTICLES = 10

def getRelatedURLs(url):
	relatedURLs = []
	# try:
	# 	response = requests.get(url, headers=hdr)
	# 	html = response.content
	# except:
	try:
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
		req = urllib2.Request(url, headers=hdr)
		html = opener.open(req)
		for link in BeautifulSoup(html, parse_only=SoupStrainer("a", href=True)).find_all("a"):
			relatedURL = link['href'].split('#')[0]
			relatedURLs.append(relatedURL)
	except:
		pass
	relatedURLs = list(set(relatedURLs))
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
	date = str(article.publish_date)
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
		content, title, authors, date = getContentFromNewspaper(url)
	except:
		try:
			content = getContentFromBoilerpipe(url)
		except:
			pass
	return content, title, authors, date

def isPotentialArticle(url):
	if (url.count('-') > 3 or url.count('+') > 3 or url.count('_') > 3 or "article" in url or "content" in url) \
			and not any(exclude in url for exclude in nonArticles):
		return True
	else:
		return False

nonArticles = ["video", "picture", "image", "facebook", "twitter", "digg", "pinterest", "mailto", "linkedin", "google"]

with open('inputSites.txt', 'r') as input, io.open('articles.txt', 'w', encoding="utf-8") as output:
	for main in input:
		main = main.strip()
		if (main[-1] == "/"):	# for concatenation of sublinks which start with "/"
			main = main[:-1]
		toVisit = [main]
		toVisitandVisited = toVisit
		listlinks = []
		relatedURLs = []
		while(len(listlinks) < MAX_ARTICLES and len(toVisit) > 0):
			url = toVisit[0]
			toVisit = toVisit[1:]
			content, title, authors, date = getContent(url)

			if (url == main) or (url != main and len(content) > MIN_ARTICLE_LENGTH):
				if len(content) > MIN_ARTICLE_LENGTH:
					data = {"main": main, "url" : url, "title" : title, "date" : date, "authors" : authors, "content" : content}
					output.write(json.dumps(data, ensure_ascii=False))
					output.write(u'\n')
					listlinks.append(url)
				
				relatedURLs = getRelatedURLs(url)
				for relatedURL in relatedURLs:
					if (isPotentialArticle(relatedURL)):
						if relatedURL[0] == "/":
							relatedURL = main + relatedURL
						elif relatedURL[0] != "h":
							relatedURL = main + "/" + relatedURL
						if main[5:] in relatedURL:						# if https links fetched but main is http
							if relatedURL not in toVisitandVisited:
								toVisit.append(relatedURL)
								toVisitandVisited.append(relatedURL)
		listlinks = []
		toVisit = []
		relatedURLs = []
		toVisitandVisited = []



