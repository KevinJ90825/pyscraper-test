# pyscraper-test

This is a high volume scraper that can be used to scrape websites using Python. It uses gevent for asynchronous requests. 

For the demo it prints out the scraped information but normally it would save these items to a database or dump the information to a file.

## To run
Use pip to install the libraries in requirements.txt (`pip install -r requirements.txt`).
Then run `python start_scraper.py` to begin scraping the current front page of Hacker News (https://news.ycombinator.com)