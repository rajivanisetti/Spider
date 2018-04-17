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

	function getValueFromCategory(category)
  		if category == "accounting" then
   		 	return "110100124"
  		elseif category == "administrative" then
    		return "210100124"
  		elseif category == "architecture/engineering" then
    		return "2110100124"
  		elseif category == "attorney" then
    		return "2210100124"
  		elseif category == "bank examiner" then
    		return "2310100124"
  		elseif category == "business analyst" then
   			return "2410100124"
  		elseif category == "computer professional" then
    		return "2510100124"
  		elseif category == "computer support" then
    		return "2610100124"
  		elseif category == "economist" then
    		return "2710100124"
  		elseif category == "editors/writers" then
    		return "2810100124"
  		elseif category == "eeo" then
    		return "310100124"
  		elseif category == "financial analyst" then
    		return "410100124"
  		elseif category == "governors" then
    		return "510100124"
  		elseif category == "graphic design" then
    		return "610100124"
  		elseif category == "health services" then
    		return "2910100124"
  		elseif category == "human resources" then
    		return "3010100124"
  		elseif category == "interns" then
    		return "3110100124"
  		elseif category == "mail services and supply" then
    		return "3210100124"
  		elseif category == "other clerical-acctg/payroll" then
    		return "3310100124"
  		elseif category == "other clerical-administration" then
    		return "3410100124"
  		elseif category == "other clerical-bldg services" then
    		return "3510100124"
  		elseif category == "other clerical-computersupport" then
    		return "3610100124"
  		elseif category == "other clerical-finance/bus an" then
    		return "3710100124"
  		elseif category == "other clerical food services" then
    		return "3810100124"
  		elseif category == "other clerical-graphics" then
    		return "3910100124"
  		elseif category == "other clerical-hr" then
    		return "4010100124"
  		elseif category == "other clerical-mail svc/supply" then
    		return "4110100124"
  		elseif category == "other clerical-other" then
    		return "4210100124"
  		elseif category == "other clerical-pr/writ/edit" then
    		return "4310100124"
  		elseif category == "other clerical-purchasing" then
    		return "4410100124"
  		elseif category == "other clerical-training" then
    		return "4510100124"
  		elseif category == "other professional" then
    		return "4610100124"
  		elseif category == "public relations" then
    		return "4710100124"
  		elseif category == "purchasing" then
    		return "4810100124"
  		elseif category == "research assistant" then
    		return "4910100124"
  		elseif category == "security administration" then
    		return "5010100124"
  		elseif category == "security escort" then
    		return "5110100124"
  		elseif category == "secrtry/steno/clerk typ/recept" then
    		return "710100124"
  		elseif category == "security admin support" then
    		return "810100124"
  		elseif category == "security" then
    		return "910100124"
  		elseif category == "trade/crafts-eng/plant" then
    		return "1010100124"
  		elseif category == "trade/crafts-food service" then
    		return "1110100124"
  		elseif category == "trade/crafts-maintenance" then
    		return "5210100124"
  		elseif category == "trade/crafts-motor transport" then
    		return "5310100124"
  		elseif category == "trade/crafts-other" then
    		return "5410100124"
  		elseif category == "trade/crafts-print/litho" then
    		return "5510100124"
  		elseif category == "trade/crafts-postal/supply" then
    		return "5610100124"
  		elseif category == "training" then
    		return "5710100124"
  		else
    		error('Invalid Category')
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







