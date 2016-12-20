import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.xpath('//*[@class="quote"]'):
            yield {
                'text': quote.xpath('.//*[@class="text"]//text()').extract_first(),
                'author': quote.xpath('.//*[@class="author"]//text()').extract_first(),
                'tags': quote.xpath('.//*[@class="tags"]/a[@class="tag"]//text()').extract(),
            }

        next_page = response.xpath('//*[@class="pager"]/li[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
