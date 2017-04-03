from bs4 import BeautifulSoup as BS
import urllib2 

mbfclinks = []		# contains urls of news website pages on MediaBiasFactCheck.com
finallist = []		# contains source names, urls, factual reporting, bias,

links = ['left/','leftcenter/','center/','right-center/', 'right/', 'pro-science/', 'conspiracy/', 'fake-news/', 'satire/']
# links = ['pro-science/']	# for testing
main = 'https://mediabiasfactcheck.com/'
hdr = { 'User-Agent' : 'super happy bot' }
for link in links:
	req = urllib2.Request(main+link, headers=hdr)
	html = urllib2.urlopen(req).read()
	soup = BS(html, "lxml")
	for text in soup.find_all('div', class_='entry clearfix'):
		for links in text.find_all('a'):
			mbfclinks.append(links.get('href'))

for url in mbfclinks:
	req = urllib2.Request(url, headers=hdr)
	html = urllib2.urlopen(req).read()
	soup = BS(html, "lxml")
	fact = ""
	bias = ""
	source = ""
	for txt in soup.find_all('h1', class_='page-title page-title-layout1'):
		if len(txt.text) < 50:
			name = txt.text
	for txt in soup.find_all('div', class_='entry-content'):
		for src in txt.find_all('p'):
			if "ource:" in src.text and len(src.text) < 60:
				source = src.text
			if "ias:" in src.text and len(src.text) < 50:
				bias = src.text
			if "Factual" in src.text and len(src.text) < 60:
				fact = src.text
	finallist.append([name,source,fact, bias])

for link in finallist:
	print u', '.join((link[0], link[1], link[2], link[3])).encode('utf-8')
