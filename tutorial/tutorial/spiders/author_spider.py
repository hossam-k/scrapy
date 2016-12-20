import scrapy

class AuthorSpider(scrapy.Spider):
    name="author"
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self,response):
        for href in response.xpath('//*[@class="quote"]/span/a/@href').extract():
            yield scrapy.Request(response.urljoin(href),callback=self.parse_author)

        next_page = response.xpath('//*[@class="pager"]/li[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            "author":response.xpath('//*[@class="author-details"]/h3[@class="author-title"]//text()').extract(),
            "birthdate":response.xpath('//*[@class="author-details"]/p/span[@class="author-born-date"]//text()').extract(),
            "bio":response.xpath('//*[@class="author-details"]/div[@class="author-description"]//text()').extract(),
        }
