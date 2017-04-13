from bs4 import BeautifulSoup as BS
import urllib2 

list = []
hdr = { 'User-Agent' : 'super friendly bot' }
with open('sitelinks.txt', 'r') as f:
	for index, line in enumerate(f):
		try:
			req = urllib2.Request(line, headers=hdr)
			html = urllib2.urlopen(req).read()
			soup = BS(html, "lxml")
			count = 0
			breaker = False
			for link in soup.find_all('a', href=True):
				if (line+', '+link['href']) not in list and 'pinterest' not in link['href'] and 'twitter' not in link['href'] and 'facebook' not in link['href'] and ('politics' in link['href'] or 'rump' in link['href']) and (line in link['href'] or link['href'][0] == '/'):
					list.append(line+', '+link['href'])
					print line+', '+link['href']
					count += 1
				if count == 5:
					breaker = True
					break
			if breaker == True:
				continue
			elif breaker == False and count == 0:
				list.append(line+', none')
				print line+', none'

		except:
			list.append(line+', error')
			print line+', error'

with open('articlelinks.txt', 'w') as f:
	for line in list:
		f.write(line)
