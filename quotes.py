import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes" #unique name for your spider

    def start_requests(self):
        urls = [
            'https://quotes.toscrape.com/page/1/',
            'https://quotes.toscrape.com/page/2/',
        ]
                       
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):  #response.css('div.quote') gets a list of quotes; everything inside tags '<div class="quote">' and '</div>' 
            yield{ #yields a dictionary
                'text': quote.css('span.text::text').get(),  #inside a quote, get everything between the tags <span class="text"> and <\span>
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(), #<a> is inside <tags> <\tags> meaning <tags> ... <a..>...<\a> <\tags>
            }

    """
    Steps to run the code:         
    1) Go to project’s top level directory 
    2) Run command: scrapy crawl crawlerName (replace crawlerName with your specified crawler's name;for this code the name is 'quotes')
    """
    
    ####### Read json file ######
    #with open('quotes.jsonl', 'r') as file:
    #    json_data = [json.loads(line) for line in file]

