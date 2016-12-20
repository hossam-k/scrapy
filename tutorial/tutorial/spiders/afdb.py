import scrapy
from scrapy.http import FormRequest
from tutorial.items import TutorialItem

class AFDBSpider(scrapy.Spider):
    name = "afdb"
    allowed_domains = ["afdb.org"]

    item_list_fields = {
        'items_table' : '//table/tbody/tr',
        'item_date' : './/td[@class="date"]//text()',
        'item_title' : './/td[@class="title"]//p/a//text()',
        'item_url' : './/td[@class="title"]//p/a/@href',
    }

    def start_requests(self):
        urls = [
            "http://www.afdb.org/en/projects-and-operations/procurement/resources-for-businesses/general-procurement-notices-gpns/",
            "http://www.afdb.org/en/projects-and-operations/procurement/resources-for-businesses/invitation-for-bids/",
            "http://www.afdb.org/en/projects-and-operations/procurement/resources-for-businesses/specific-procurement-notices-spns/",
            "http://www.afdb.org/en/projects-and-operations/procurement/resources-for-businesses/expressions-of-interest-for-consultants/",
            "http://www.afdb.org/en/projects-and-operations/procurement/resources-for-businesses/procurement-plans/",
        ]
        for url in urls:
            #filtering search results for information and technology topics
            yield  FormRequest(url=url,
                     formdata={'tx_llcatalog_pi[filters][countries][]': 'all', 'tx_llcatalog_pi[filters][themes][]': '648', 'tx_llcatalog_pi[filters][search]':'search'},
                     callback=self.parse)

    def parse(self, response):
        item_list_selector = response.xpath(self.item_list_fields["items_table"])
        for sel in item_list_selector:
            tender_title = sel.xpath(self.item_list_fields['item_title']).extract_first()
            tender_date =  sel.xpath(self.item_list_fields['item_date']).extract_first()
            tender_url = "http://www.afdb.org" + sel.xpath(self.item_list_fields['item_url']).extract_first()
            #creating item for each tender
            tutorialItem=TutorialItem()
            tutorialItem['title'] = tender_title
            tutorialItem['date'] = tender_date
            tutorialItem['url'] = tender_url
            yield (tutorialItem)

        next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            print "next_page" + next_page
            next_page=response.urljoin(next_page)
            yield scrapy.Request(next_page, callback = self.parse)
