# Rudimentary scraper; change query variable to a new URL to scrape (include the 'http://' part)
# Also, you might need to pip install BeautifulSoup and nltk corpus for English stop words

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import requests

query = 'http://www.cnn.com/2017/04/02/politics/donald-trump-north-korea'

req = requests.get(query, headers={ 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11' })
html = req.text
soup = BeautifulSoup(html, 'lxml')
[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
visible_text = soup.getText(separator=' ')
words = visible_text.split()
filtered_words = [word for word in words if word not in stopwords.words('english')]
filtered_words = ' '.join(filtered_words)

print filtered_words
