import re

import requests
from gevent.threading import Lock
from pyquery import PyQuery
import gevent
import logging
from gevent.pool import Pool

class ScraperBase(object):

    SCRAPER_WORKERS = 5
    DATABASE_WORKERS = 15

    LOGGER = logging.getLogger(__name__)

    all_items = []
    max_shares = 0
    lock = Lock()
    error_count = 0

    def __init__(self):

        if not hasattr(self, 'base_url'):
            raise NotImplementedError("Scraper must have a base URL")

        if not hasattr(self, 'start_url'):
            raise NotImplementedError("Scraper must have a start URL")

        if not hasattr(self, 'start_scraper'):
            raise NotImplementedError("Scraper must have start_scraper callback")

        self._requests_pool = Pool(self.SCRAPER_WORKERS)
        self._database_pool = Pool(self.DATABASE_WORKERS)

    def start_scraper(self):
        self._submit_request(
            self.start_url,
            callback=self.start_scraper_callback
        )

        gevent.wait()

        self.LOGGER.info("Requests free: {}".format(self._requests_pool.free_count()))
        self.LOGGER.info("Database free: {}".format(self._database_pool.free_count()))

    def _get_selector(self, response):
        try:
            pq = PyQuery(response.content)
            pq.make_links_absolute(response.url)
        except Exception, e:
            self.LOGGER.warn(e)
            self.error_count += 1
            return None
        return pq

    def _greenlet_request(self, url, method, info_dict=None, callback=None, request_data=None, **kwargs):
        if method == 'GET':
            return requests.get(url, **kwargs), info_dict, callback
        elif method == 'POST':
            if not request_data:
                request_data = {}

            return requests.post(url, request_data, **kwargs), info_dict, callback

    def _greenlet_callback(self, green):
        response, info, callback = green.value

        if callback:
            callback(response, self._get_selector(response), info)

    def _submit_request(self, url, info_dict=None, callback=None, method='GET', request_data=None, **kwargs):

        green = self._requests_pool.spawn(
            self._greenlet_request,
            url,
            method=method,
            info_dict=info_dict,
            callback=callback,
            request_data=request_data,
            **kwargs
        )

        if callback:
            green.link(self._greenlet_callback)
