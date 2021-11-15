import scrapy
from VacancyParse.items import VacancyparseItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&salary=95000&only_with_salary=true&area=113&experience=between3And6&search_field=description&search_field=company_name&search_field=name',
                  'https://hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&salary=95000&only_with_salary=true&area=113&experience=between1And3&search_field=description&search_field=company_name&search_field=name',
                  'https://hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&salary=95000&only_with_salary=true&area=113&experience=noExperience&search_field=description&search_field=company_name&search_field=name',
                  'https://hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&salary=95000&only_with_salary=true&area=113&experience=moreThan6&search_field=description&search_field=company_name&search_field=name',
                  'https://hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&salary=180000&only_with_salary=true&area=113&experience=between3And6&search_field=description&search_field=company_name&search_field=name',
                  'https://hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&salary=180000&only_with_salary=true&area=113&experience=between1And3&search_field=description&search_field=company_name&search_field=name',
                  'https://hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&salary=180000&only_with_salary=true&area=113&experience=moreThan6&search_field=description&search_field=company_name&search_field=name',
                  'https://hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&salary=180000&only_with_salary=true&area=113&experience=noExperience&search_field=description&search_field=company_name&search_field=name',
                  'https://hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&salary=265000&only_with_salary=true&area=113&search_field=description&search_field=company_name&search_field=name',
                  'https://hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&salary=350000&only_with_salary=true&area=113&search_field=description&search_field=company_name&search_field=name',
                  'https://hh.ru/search/vacancy?fromSearchLine=true&text=Python&from=suggest_post&salary=435000&only_with_salary=true&area=113&search_field=description&search_field=company_name&search_field=name',]

    def parse(self, response):

        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response):
        name = response.xpath('//h1/text()').get()
        salary = response.xpath('//div[@class="vacancy-salary"]/span/text()').getall()
        url = response.url
        yield VacancyparseItem(name=name, salary=salary, url=url)