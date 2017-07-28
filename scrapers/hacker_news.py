
from scrapers.common import ScraperBase
import urlparse


class HNScraper(ScraperBase):
    base_url = 'https://news.ycombinator.com/'
    start_url = base_url
    source = "HN"

    comments_base = urlparse.urljoin(base_url, "item?id={}")

    def start_scraper_callback(self, response, selector, info_dict):
        for news_item in selector("tr.athing").items():
            info_dict = {
                'title': news_item(".title").text(),
                'link': news_item("a.storylink").attr("href"),
                'news_id': news_item.attr("id")
            }

            comments_url = self.comments_base.format(info_dict['news_id'])

            self._submit_request(
                url=comments_url,
                callback=self._parse_comments,
                info_dict=info_dict
            )

    def _parse_comments(self, response, selector, info_dict):
        top_comment = selector('.athing.comtr:first').text()
        info_dict['top_Comment'] = top_comment
        print info_dict
        x=3
