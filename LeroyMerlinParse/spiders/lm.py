import scrapy
from scrapy.loader import ItemLoader
from LeroyMerlinParse.items import LeroymerlinparseItem


class LmSpider(scrapy.Spider):
    name = 'lm'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/search/?q=двери']

    def parse(self, response):
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//a[@data-qa="product-name"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.item_parse)

    def item_parse(self, response):
        loader = ItemLoader(item=LeroymerlinparseItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_value('link', response.url)
        loader.add_xpath('photos', "//img[@alt='product image']/@src")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        yield loader.load_item()