# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from importlib import import_module

from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware

from stem import Signal
from stem.control import Controller

class ProxyMiddleware(HttpProxyMiddleware):
    """Scrapy middleware for issuing a new IP address if necessary"""

    def __init__(self, proxy_url, proxy_pass, ban_sites):
        self.proxy_url = proxy_url
        self.proxy_pass = proxy_pass
        self.ban_sites = ban_sites
        super(ProxyMiddleware, self).__init__()

    @classmethod
    def from_crawler(cls, crawler):
        proxy_url = crawler.settings.get('PROXY_URL')
        proxy_pass = crawler.settings.get('PROXY_PASSWORD')
        ban_sites = crawler.settings.get('IP_BAN_SITES')
        if not proxy_url or not proxy_pass or not ban_sites:
            raise NotConfigured('PROXY_URL, PROXY_PASSWORD, and IP_BAN_SITES must be set')
        middleware = cls(
            proxy_url = proxy_url,
            proxy_pass = proxy_pass,
            ban_sites = ban_sites
        )
        return middleware

    def new_tor_identity(self):
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password=self.proxy_pass)
            controller.signal(Signal.NEWNYM)

    def process_request(self, request, spider):
        url = request.url
        for ban_site in self.ban_sites:
            if ban_site in url:
                self.new_tor_identity()
                request.meta['proxy'] = self.proxy_url