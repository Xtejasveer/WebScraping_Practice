import scrapy


class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["www.audible.com"]
    start_urls = ["https://www.audible.com/search"]

    custom_settings = {
        'REDIRECT_ENABLED': False,  # prevent redirect to audible.in
    }

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.audible.com/search",
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            },
            meta={'dont_redirect': True},
            callback=self.parse
        )

    def parse(self, response):
        # print("Current URL:", response.url)  # verify no redirect happened
        # print("Status Code:", response.status)
        product_container = response.xpath('//div[@class="adbl-impression-container "]/div/span/ul/li')

        for product in product_container:
            book_title = product.xpath('.//h3[contains(@class, "bc-heading")]/a/text()').get()
            book_author = product.xpath('.//li[contains(@class, "authorLabel")]/span/a/text()').getall()  ## beacuse a book can have more than one author that is why we used getall() function
            book_length = product.xpath('.//li[contains(@class, "runtimeLabel")]/span/text()').get()

            yield {
                'title' : book_title,
                'author' : book_author,
                'Runtime' : book_length,
            }

            pagination = response.xpath("//ul[contains(@class, 'pagingElements')]")
            next_page_url = pagination.xpath(".//span[contains(@class, 'nextButton')]/a/@href").get()

            if next_page_url:
                yield response.follow(url = next_page_url, callback = self.parse)