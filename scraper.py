import scrapy
from scrapy import *
import requests as r
from requests_html import HTMLSession
import urllib
from bs4 import BeautifulSoup
import json
from lxml import html

#Amazon
amazon = {}
amazon["query_str_append"] = "s?k="
amazon["home"] = "https://www.amazon.in/"

amazon["query_str_append"] = "s?k="

amazon["products_selector"] = "//img[@data-image-index]"
amazon["href_selector"] = "./ancestor::a/@href"
amazon["name_selector"] = "./@alt"
amazon["image_selector"] = "./@src"
#amazon["price_selector"] = "./descendant::div[@class='style__price-tag___KzOkY']/text()"


query = "handwash"                  #get this from user


#Flipkart
flipkart = {}
flipkart["home"] = "https://www.flipkart.com/"
flipkart["query_str_append"] = "search?q="

flipkart["products_selector"] = "//a[@class='Zhf2z-']"
flipkart["href_selector"] = "./@href"
flipkart["name_selector"] = "./descendant::img[@class='_1Nyybr _30XEf0']/@alt"
flipkart["image_selector"] = "./descendant::img[@class='_1Nyybr _30XEf0']/@src"
#flipkart["price_selector"] = "./descendant::div[@class='style__price-tag___KzOkY']/text()"


#1mg
#Looks like 1mg renders dynamic content - can't get the names and images of products
#but am able to get the product urls though - nah, the urls don't work too
_1mg = {}
_1mg["home"] = "https://www.1mg.com/"
_1mg["query_str_append"] = "search/all?name="

_1mg["products_selector"] = "//a[@class='style__product-link___1hWpa']"
_1mg["href_selector"] = "./@href"
_1mg["name_selector"] = "./descendant::img[@class='style__image___Ny-Sa style__loaded___22epL']/@alt"
_1mg["image_selector"] = "./descendant::img[@class='style__image___Ny-Sa style__loaded___22epL']/@src"
_1mg["price_selector"] = "./descendant::div[@class='style__price-tag___KzOkY']/text()"

site = _1mg


#Netmeds
#some POST data that I can't figure
netmeds = {}
netmeds["home"] = "https://www.netmeds.com/"
netmeds["query_str_append"] = "catalogsearch/result?q="

netmeds["products_selector"] = "//li[@class='ais-InfiniteHits-item']"
netmeds["href_selector"] = "./descendant::div[@class='drug_c']/a/@href"
netmeds["name_selector"] = "./descendant::div[@class='info']/text()"
netmeds["image_selector"] = "./descendant::div[@class='drug_img']/img/@src"
netmeds["price_selector"] = "./descendant::span[@class='final-price']/text()"
netmeds["drug-manufacturer"] = "./descendant::span[@class='drug-manu']/text()"

site = netmeds

query = "globac z"

#BigBasket
bigbasket = {}
bigbasket["home"] = "https://www.bigbasket.com/"
bigbasket["query_str_append"] = "ps/?q="
bigbasket["products_selector"] = "//li[@qa='product']"
bigbasket["href_selector"] = "./descendant::div[@class='uiv2-list-box-img-block']/a/@href"
bigbasket["name_selector"] = "./descendant::div[@class='uiv2-list-box-img-block']/a/@title"
bigbasket["image_selector"] = "./descendant::div[@class='uiv2-list-box-img-block']/a/img/@src"
bigbasket["price_selector"] = "./descendant::div[@qa='priceRP']/text()"

site = bigbasket
query = "handwash"

#Common code for all sites
# just give the site dict
site = amazon
query = "handwash"

site = netmeds
query = "globac z"

site = bigbasket
query = "handwash"

query = query.replace(" ","+")              # - replace space with '+'
final_url = site["home"] + site["query_str_append"] + query

s = HTMLSession()
# s.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0'}
page = s.get(final_url)
# print(response.text)
# response = urllib.request.urlopen(final_url)
# soup = BeautifulSoup(response,'html.parser')
# page = r.get(final_url)

tree = html.fromstring(page.content)
response = {}
for p in tree.xpath(site["products_selector"]):
    response["name"] = p.xpath(site["name_selector"])[0]                #.extract_first()
    response["image"] = p.xpath(site["image_selector"])[0]              #.extract_first()
    response["hyperlink"] = site["home"] + p.xpath(site["href_selector"])[0]
    #price = p.xpath(site["price_selector"])[0]        #.extract()[-1]
    try:
        response["manufacturer"] = p.xpath(site["drug-manufacturer"])[0]         #.extract_first()
    except:
        pass
    print(response)


