# Social Networks Spring 2017
fake news crüe

## Dependencies
* [scrapy](https://scrapy.org/)
* [boilerpipe](https://github.com/misja/python-boilerpipe)

## Usage

### Crawling
`python run.py crawl [-c count]`

__Optional Arguments:__
* COUNT: Number of items to limit crawl (Default: 10)

__Important Files/Directories:__
* crawler/urls.py: Site urls to begin crawler
* crawler/rules.py: Regex rules to extract article urls
* articles/*__domain__*/html/*__url_hash__*.html: Extracted article html file 
* articles.json: List of extracted articles (url, domain, title, file path)

### Extracting
`python run.py extract [--html]`

__Optional Arguments:__
* HTML: Flag to have extractor use local html instead of urls (Default: false)

__Important Files/Directories:__
* articles.json: Required to run extractor with urls or html
* articles/*__domain__*/text/*__url_hash__*.txt: Extracted article text file 