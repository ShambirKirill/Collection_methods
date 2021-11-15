# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

class VacancyparsePipeline:

    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.db = client['VacancyParse']

    def process_item(self, item, spider):
        item['salary'] = self.process_salary(item['salary'])
        item['_id'] = item['url'].split('?')[0].split('/')[-1]
        item['min_wage'] = item['salary'][0]
        item['max_wage'] = item['salary'][1]
        item['currency'] = item['salary'][2]
        item.pop('salary')
        try:
            collection = self.db[spider.name]
            collection.insert_one(item)
        except dke:
            pass
        return item

    def process_salary(self, salary):

        if salary:
            cleaning = []
            first_el = salary[0].replace(' ', '') # Нужно определить от, до, или вообще нет. Удаляю пробелы для hh.ru
            for i in salary:
                i = i.split('\xa0')
                for el in i:
                    if el in ['руб.', 'EUR', 'USD']:
                        currency = el
            try:
                for i in salary:
                    i = i.split('\xa0')
                    for el in i:
                        if el.isdigit() == True:
                            cleaning.append(el)

                if len(cleaning) == 2:
                    if first_el == 'до':
                        min_wage = None
                        max_wage = int(cleaning[0] + cleaning[1])
                        return min_wage, max_wage, currency
                    elif first_el == 'от':
                        min_wage = int(cleaning[0] + cleaning[1])
                        max_wage = None
                        return min_wage, max_wage, currency
                    else: # на SJ есть фиксированые зарплаты. Они являются максимальными зп
                        min_wage = None
                        max_wage = int(cleaning[0] + cleaning[1])
                        return min_wage, max_wage, currency
                elif len(cleaning) == 4:
                        min_wage = int(cleaning[0] + cleaning[1])
                        max_wage = int(cleaning[2] + cleaning[3])
                        return min_wage, max_wage, currency
            except:
                pass
        else:
            min_wage = None
            max_wage = None
            currency = None
            return min_wage, max_wage, currency

