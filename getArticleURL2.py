import requests, json
from bs4 import BeautifulSoup

def getHTML(url):
    response = requests.get(url)
    # parse html
    page = str(BeautifulSoup(response.content))
    return page

def getURL(page):
    """

    :param page: html of web page (here: Python home page) 
    :return: urls in that page 
    """
    start_link = page.find("a href")
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url, end_quote

listlinks = []
pagestovisit = ["http://www.voanews.com/"]

while(len(listlinks) < 250 and len(pagestovisit) > 0):
    print(len(listlinks))
    url = pagestovisit[0]
    pagestovisit = pagestovisit[1:]
    page = getHTML(url)

    while True:
        url, n = getURL(page)
        page = page[n:]
        if url:
            if (url.find("/a/") == 0):
                print url
                listlinks.append("http://www.voanews.com" + url)
                pagestovisit.append("http://www.voanews.com" + url)
                listlinks = list(set(listlinks))
        else:
            break

output = ""
for i in listlinks:
    output = output + i + ', '
json.dump(output, open("links.txt", 'w'))

