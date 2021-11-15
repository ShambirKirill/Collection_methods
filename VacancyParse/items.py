# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VacancyparseItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    url = scrapy.Field()
    min_wage = scrapy.Field()
    max_wage = scrapy.Field()
    currency = scrapy.Field()
