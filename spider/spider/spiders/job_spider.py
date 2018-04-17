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
  if category == "Accounting" then
    return "110100124"
  elseif category == "Administrative" then
    return "210100124"
  elseif category == "Architecture/Engineering" then
    return "2110100124"
  elseif category == "Attorney" then
    return "2210100124"
  elseif category == "Bank Examiner" then
    return "2310100124"
  elseif category == "Business Analyst" then
    return "2410100124"
  elseif category == "Computer Professional" then
    return "2510100124"
  elseif category == "Computer Support" then
    return "2610100124"
  elseif category == "Economist" then
    return "2710100124"
  elseif category == "Editors/Writers" then
    return "2810100124"
  elseif category == "EEO" then
    return "310100124"
  elseif category == "Financial Analyst" then
    return "410100124"
  elseif category == "Governors" then
    return "510100124"
  elseif category == "Graphic Design" then
    return "610100124"
  elseif category == "Health Services" then
    return "2910100124"
  elseif category == "Human Resources" then
    return "3010100124"
  elseif category == "Interns" then
    return "3110100124"
  elseif category == "Mail Services and Supply" then
    return "3210100124"
  elseif category == "Other Clerical-Acctg/Payroll" then
    return "3310100124"
  elseif category == "Other Clerical-Administration" then
    return "3410100124"
  elseif category == "Other Clerical-Bldg Services" then
    return "3510100124"
  elseif category == "Other Clerical-ComputerSupport" then
    return "3610100124"
  elseif category == "Other Clerical-Finance/Bus An" then
    return "3710100124"
  elseif category == "Other Clerical Food Services" then
    return "3810100124"
  elseif category == "Other Clerical-Graphics" then
    return "3910100124"
  elseif category == "Other Clerical-HR" then
    return "4010100124"
  elseif category == "Other Clerical-Mail Svc/Supply" then
    return "4110100124"
  elseif category == "Other Clerical-Other" then
    return "4210100124"
  elseif category == "Other Clerical-PR/Writ/Edit" then
    return "4310100124"
  elseif category == "Other Clerical-Purchasing" then
    return "4410100124"
  elseif category == "Other Clerical-Training" then
    return "4510100124"
  elseif category == "Other Professional" then
    return "4610100124"
  elseif category == "Public Relations" then
    return "4710100124"
  elseif category == "Purchasing" then
    return "4810100124"
  elseif category == "Research Assistant" then
    return "4910100124"
  elseif category == "Security Administration" then
    return "5010100124"
  elseif category == "Security Escort" then
    return "5110100124"
  elseif category == "Secrtry/Steno/Clerk Typ/Recept" then
    return "710100124"
  elseif category == "Security Admin Support" then
    return "810100124"
  elseif category == "Security" then
    return "910100124"
  elseif category == "Trade/Crafts-Eng/Plant" then
    return "1010100124"
  elseif category == "Trade/Crafts-Food Service" then
    return "1110100124"
  elseif category == "Trade/Crafts-Maintenance" then
    return "5210100124"
  elseif category == "Trade/Crafts-Motor Transport" then
    return "5310100124"
  elseif category == "Trade/Crafts-Other" then
    return "5410100124"
  elseif category == "Trade/Crafts-Print/Litho" then
    return "5510100124"
  elseif category == "Trade/Crafts-Postal/Supply" then
    return "5610100124"
  elseif category == "Training" then
    return "5710100124"
  else
    error('Invalid category')
  end
end
    


function main(splash, args)
  -- find a form and submit "splash" to it
  local function search_for_splash()
    local inputs = splash:select_all('input')

    if #forms ~= 0 then
      error('found ya')
    end

    local form, input = find_input(forms)

    if not input then
      error('no search form is found')
    end

    assert(input:send_keys('splash'))
    assert(splash:wait(0))
    assert(form:submit())
  end
  
  function dropdown(category)
  	local js = string.format("document.getElementById('advancedSearchInterface\\.jobfield1L1').value = %s;", getValueFromCategory(category))
  	assert(splash:runjs(js))
	end

  -- main rendering script
  assert(splash:go(args.url))
  assert(splash:wait(5))
  local inputs = splash:select_all('input.inputbutton')
  local searches = splash:select_all('input')
  local keywordSearch = findSearch(searches)
 
  local category = "Attorney"
  local value = getValueFromCategory(category)
      
  dropdown(category)

  local searchButton = findButton(inputs)
  
  
  assert(keywordSearch:send_keys('attorney'))
  assert(splash:wait(1.0))
  
  searchButton:mouse_click()
  
  assert(splash:wait(3))

  local scroll_to = splash:jsfunc("window.scrollTo")
  scroll_to(0, 300)
  return splash:png()
end



	"""

	def __init__(self, category=None, keyword=None *args, **kwargs):
		super(JobSpider, self).__init__(*args, **kwargs)
		self.category = category
		self.keyword = keyword

	def start_requests(self):
		yield SplashRequest(url = 'https://frbog.taleo.net/careersection/1/moresearch.ftl?lang=en&portal=101430233', callback = self.parse, 'endpoint' = 'execute', category = self.category, keyword = self.keyword)

	def parse(self, response):



