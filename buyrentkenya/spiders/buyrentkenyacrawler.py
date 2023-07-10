import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BuyrentkenyacrawlerSpider(CrawlSpider):
    name = 'buyrentkenyacrawler'
    allowed_domains = ['buyrentkenya.com']
    start_urls = ['https://www.buyrentkenya.com/houses-for-sale']

    rules = (
        ## follow pagination links
        Rule(LinkExtractor(allow=r'(houses-for-sale\?page=\d+$)')),
        ## follow links to house pages
        Rule(LinkExtractor(allow=r'(listings/).*(-\d+$)'), callback='parse_listing', follow=True),

    )

    def parse_listing(self, response):
        yield {
            # 'house_name': house_name,
            'listing_title': response.xpath('//h1[@data-cy="listing-heading"]/text()').get().strip(),
            'location': response.xpath('(//div/p[@data-cy="listing-address"]/text())[3]').get().strip(),
            'price': response.xpath('//span[@aria-label="price"]/text()').get().strip(),
            'land_area': response.xpath('//span[@aria-label="area"]/text()').get(),
            'bedrooms': response.xpath('(//span[@aria-label="bedrooms"]/text())[2]').get(),
            'bathrooms': response.xpath('(//span[@aria-label="bathrooms"]/text())[2]').get(),
            'agent_name': response.xpath('//img[@data-cy="agency-image"]/@alt').get(),
            'date_created': response.xpath('//span[@date-cy="date-created"]/text()').get(),
            'internal_features': response.xpath(
                '(//div[@class="flex flex-col pb-2"])[1]/ul[@class="items-center flex flex-row flex-wrap"]/li/div/text()').getall(),
            'external_features': response.xpath(
                '(//div[@class="flex flex-col pb-2"])[2]/ul[@class="items-center flex flex-row flex-wrap"]/li/div/text()').getall(),
            'nearby': response.xpath(
                '(//div[@class="flex flex-col pb-2"])[3]/ul[@class="items-center flex flex-row flex-wrap"]/li/div/text()').getall(),
            'link': response.url,
        }
