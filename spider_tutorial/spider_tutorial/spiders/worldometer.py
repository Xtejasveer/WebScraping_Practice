import scrapy


class WorldometerSpider(scrapy.Spider):
    name = "worldometer"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):
        # title = response.xpath('//h1/text()').get()

        countries = response.xpath('//td/a')
        for country in countries:
            country_name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            abs_link =  response.urljoin(link)
            
            yield scrapy.Request(url = abs_link, callback = self.parse_country, meta = {'country' : country_name})

    def parse_country(self, response):
        rows = response.xpath('(//table[contains(@class,"table")])[1]/tbody/tr')
        country = response.request.meta['country']
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/text()').get()

            yield{
                'country':country,
                'year' : year,
                'population' : population,
            }

