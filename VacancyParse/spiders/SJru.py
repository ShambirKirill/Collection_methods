import scrapy
from VacancyParse.items import VacancyparseItem

class SjruSpider(scrapy.Spider):
    name = 'SJru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response):
        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//span[contains(@class, "text-company-item-salary")]/../span/a/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response):
        name = response.xpath('//h1/text()').get()
        salary = response.xpath('//h1/../span/span/span/text()').getall()
        url = response.url
        yield VacancyparseItem(name=name, salary=salary, url=url)
