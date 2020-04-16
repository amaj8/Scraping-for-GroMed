#!/usr/bin/python3
import scrapy
from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.utils.project import get_project_settings

from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings
from scrapy import signals
from scrapy.signalmanager import dispatcher

# results = []
# class ItemCollectorPipeline(object):
#     def __init__(self):
#         self.ids_seen = set()
#
#     def process_item(self, item, spider):
#         results.append(item)

class AmazonExtract:
    def __init__(self):

        #Amazon
        amazon = {}
        amazon["query_str_append"] = "s?k="
        amazon["home"] = "https://www.amazon.in/"
        amazon["query_str_append"] = "s?k="

        amazon["products_selector"] = "//div[@data-index]"
        amazon["href_selector"] = "./descendant::a[@class='a-link-normal']/@href"
        amazon["image_selector"] = "./descendant::img[@class='s-image']/@src"
        amazon["name_selector"] = "./descendant::img[@class='s-image']/@alt"
            # "./descendant::span[@class='a-size-base-plus a-color-base a-text-normal']/text()"

        amazon["price_selector"] = "./descendant::span[@class='a-price-whole']/text()"
        self.amazon = amazon
        self.data = []

    def extract(self, query):
        site = self.amazon
        query = query.replace(" ", "+")  # - replace space with '+'
        final_url = site["home"] + site["query_str_append"] + query

        class shoppingSpider(scrapy.Spider):
            name = "shopping"
            # site = amazon
            allowed_domains = [site["home"]]
            start_urls = [final_url]


            def parse(self, response):
                item = {}
                for p in response.xpath(site["products_selector"]):
                    item["name"] = p.xpath(site["name_selector"]).extract_first()
                    item["image"] = p.xpath(site["image_selector"]).extract_first()
                    item["hyperlink"] = site["home"] + p.xpath(site["href_selector"]).extract_first()
                    item["price"] = p.xpath(site["price_selector"]).extract_first()  # .extract() #[-1]
                    try:
                        item["manufacturer"] = p.xpath(site["drug-manufacturer"]).extract_first()
                    except:
                        pass
                    yield item

        def spider_results():
            results = []

            def crawler_results(signal, sender, item, response, spider):
                results.append(item)

            # dispatcher.connect(crawler_results, signal=signals.item_passed)

            # process = CrawlerProcess({
            #     'ITEM_PIPELINES': {'__main__.ItemCollectorPipeline':100}
            # })
            crawler = Crawler(shoppingSpider)
            crawler.signals.connect(crawler_results,signals.item_scraped)

            process = CrawlerProcess(get_project_settings())
            process.crawl(crawler)
            process.start()  # the script will block here until the crawling is finished
            return results

        return spider_results()


if __name__ == '__main__':
    query = "soap"
    amazon_extractor = AmazonExtract()
    results = amazon_extractor.extract(query)
    for item in results:
        print(item)


# site = amazon
# query = "handwash"
#
# query = query.replace(" ","+")              # - replace space with '+'
# final_url = site["home"] + site["query_str_append"] + query
#
# class shoppingSpider(scrapy.Spider):
#     name = "shopping"
#     # site = amazon
#     allowed_domains = [site["home"]]
#     start_urls = [final_url]
#
#     def parse(self, response):
#         item = {}
#         for p in response.xpath(site["products_selector"]):
#             item["name"] = p.xpath(site["name_selector"]).extract_first()
#             item["image"] = p.xpath(site["image_selector"]).extract_first()
#             item["hyperlink"] = site["home"] + p.xpath(site["href_selector"]).extract_first()
#             item["price"] = p.xpath(site["price_selector"])#.extract() #[-1]
#             try:
#                 item["manufacturer"] = p.xpath(site["drug-manufacturer"]).extract_first()
#             except:
#                 pass
#             yield item
#
# process = CrawlerProcess()
# process.crawl(shoppingSpider)
# # process.crawl(MySpider2)
# process.start() # the script will block here until all crawling jobs are finished
