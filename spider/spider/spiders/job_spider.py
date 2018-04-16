import scrapy
from scrapy_splash import SplashRequest


class JobSpider(scrapy.Spider):
	name = "jobs"

	def __init__(self, category=None, keyword=None *args, **kwargs):
		super(JobSpider, self).__init__(*args, **kwargs)
		self.category = category
		self.keyword = keyword

	def start_requests(self):
		yield SplashRequest(url = 'https://www.federalreserve.gov/start-job-search.htm', callback = self.parse)

	def parse(self, response):



