# Social Networks Spring 2017
fake news crüe

## Crawling

### Dependencies
`pip install <dependency>`

* [scrapy](https://scrapy.org/)

### Usage
`python run.py crawl  [-c count]`

__Optional Arguments:__
* COUNT: Number of items to limit crawl (Default: 10)

__Important Files/Directories:__
* crawler/urls.py: Site urls to begin crawler
* crawler/rules.py: Regex rules to extract article urls
* articles/*domain*/*url_hash*.html: Extracted article html file 
* articles.json: List of extracted articles (url, domain, title, file path)