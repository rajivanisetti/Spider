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



