from scrapers.hacker_news import HNScraper

if __name__ == "__main__":

    from gevent import monkey
    monkey.patch_all()

    import psycogreen.gevent
    psycogreen.gevent.patch_psycopg()

    scraper = HNScraper()
    scraper.start_scraper()