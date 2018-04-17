# Developed by Rajiv Anisetti
# Email: rajiv.anisetti@gmail.com
# Website: www.rajivanisetti.com

import scrapy
from scrapy_splash import SplashRequest

class JobSpider(scrapy.Spider):
	name = "jobs"

	myscript= """

	function findButton(inputs)
  		for _, input in ipairs(inputs) do
    		if input.node.attributes.title == "Search for jobs matching the specified criteria" then
      			return input
    		end
  		end
	end

	function findSearch(searches)
  		for _, search in ipairs(searches) do
    		if search.node.attributes.name == "keyword" then
      			return search
    		end
  		end
	end

	local categories = {
      ["accounting"] = "110100124",
      ["administrative"] = "210100124",
      ["architecture/engineering"] = "2110100124",
      ["attorney"] = "2210100124",
      ["bank examiner"] = "2310100124",
      ["business analyst"] = "2410100124",
      ["computer professional"] = "2510100124",
      ["computer support"] = "2610100124",
      ["economist"] = "2710100124",
      ["editors/writers"] = "2810100124",
      ["eeo"] = "310100124",
      ["financial analyst"] = "410100124",
      ["governors"] = "510100124",
      ["graphic design"] = "610100124",
      ["health services"] = "2910100124",
      ["human resources"] = "3010100124",
      ["interns"] = "3110100124",
      ["mail services and supply"] = "3210100124",
      ["other clerical-acctg/payroll"] = "3310100124",
      ["other clerical-administration"] = "3410100124",
      ["other clerical-bldg services"] = "3510100124",
      ["other clerical-computersupport"] = "3610100124",
      ["other clerical-finance/bus an"] = "3710100124",
      ["other clerical food services"] = "3810100124",
      ["other clerical-graphics"] = "3910100124",
      ["other clerical-hr"] = "4010100124",
      ["other clerical-mail svc/supply"] = "4110100124",
      ["other clerical-other"] = "4210100124",
      ["other clerical-pr/writ/edit"] = "4310100124",
      ["other clerical-purchasing"] = "4410100124",
      ["other clerical-training"] = "4510100124",
      ["other professional"] = "4610100124",
      ["public relations"] = "4710100124",
      ["purchasing"] = "4810100124",
      ["research assistant"] = "4910100124",
      ["security administration"] = "5010100124",
      ["security escort"] = "5110100124",
      ["secrtry/steno/clerk typ/recept"] = "710100124",
      ["security admin support"] = "810100124",
      ["security"] = "910100124",
      ["trade/crafts-eng/plant"] = "1010100124",
      ["trade/crafts-food service"] = "1110100124",
      ["trade/crafts-maintenance"] = "5210100124",
      ["trade/crafts-motor transport"] = "5310100124",
      ["trade/crafts-other"] = "5410100124",
      ["trade/crafts-print/litho"] = "5510100124",
      ["trade/crafts-postal/supply"] = "5610100124",
      ["training"] = "5710100124"
  	}

  	function getValueFromCategory(category)
  		local value = categories[category]
      	if value == nil then
        	error('Invalid Category!')
       	else
       		return value
      	end
	end
    

	function main(splash, args)
  
  		local function dropdown(category)
  			local js = "document.getElementById('advancedSearchInterface.jobfield1').value = ".. getValueFromCategory(category) ..";"
  			assert(splash:runjs(js))
		end

  		-- main rendering script
  		assert(splash:go(args.url))
  		assert(splash:wait(5))
  		local inputs = splash:select_all('input.inputbutton')
  		local searches = splash:select_all('input')
  		local keywordSearch = findSearch(searches)
 
  		local UPcategory = args.category
  		local category = string.lower(UPcategory)
  		local searchQuery = args.keyword

	  	local function copyToSearch(searchQuery)
	  		for i = #searchQuery, 1, -1 do
	    		local char = searchQuery:sub(i,i)
	    		if char == ' ' then
	      			assert(keywordSearch:send_keys("<Space>"))
	      		else
	        		assert(keywordSearch:send_keys(char))
	       		end
	 		end
	  	end
  
  		if UPcategory ~= "None" then
  			dropdown(category)
  			assert(splash:wait(2.0))
  		end

  		local searchButton = findButton(inputs)
  
  		if searchQuery ~= "None" then
  			copyToSearch(searchQuery)
  			assert(splash:wait(1.0))
  		end
  
  		searchButton:mouse_click()
  		assert(splash:wait(3))
  		return splash:html()
	end

	"""

	def __init__(self, category="None", keyword="None", *args, **kwargs):
		super(JobSpider, self).__init__(*args, **kwargs)
		self.category = category
		self.keyword = keyword

	def start_requests(self):
		yield SplashRequest(url="https://frbog.taleo.net/careersection/1/moresearch.ftl?lang=en&portal=101430233", callback=self.parse, endpoint='execute', args={'lua_source': self.myscript, 'category':self.category, 'keyword':self.keyword})

	def parse(self, response):
		for job in response.css("span.titlelink"):
			yield {
				'Job Listing': job.css("a::text").extract()
			}







