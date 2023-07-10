import scrapy


class ForsaleSpider(scrapy.Spider):
    name = 'forSale'
    allowed_domains = ['www.buyrentkenya.com']
    start_urls = ['https://www.buyrentkenya.com/houses-for-sale']

    def parse(self, response):
        house_listing = response.xpath('//div[@class="md:w-4/5"]')

        for house in house_listing:
            house_name = house.xpath('.//h3/a/span/text()').get().strip()
            link = house.xpath('.//h3/a[contains( @ href, "listing")]/@ href').get()

            yield response.follow(url=link, callback=self.parse_house, meta={'house_name': house_name})

        # Getting the pagination bar (pagination) and then the link within the next page button (next_page_url)
        next_page = response.xpath('(//a[contains(@class, "p-3")]/@href)[5]').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)

    def parse_house(self, response):

        yield {
            'listing_title': response.request.meta['house_name'],
            'price': response.xpath('//span[@aria-label="price"]/text()').get(),
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
