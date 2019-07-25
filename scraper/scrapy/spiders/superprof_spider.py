import scrapy
from scraper.items import SuperProfItem
from scrapy.selector import Selector
from selenium import webdriver
import time
import re

class SuperProfSpider(scrapy.Spider):
    name = "superprof"

    def __init__(self):
        self.driver = webdriver.Firefox()

    def start_requests(self):
        search_topic = "anglais"
        search_location_full = "Paris--France,48.85661400000001,2.3522219000000177"
        #Paris--France,48.85661400000001,2.3522219000000177
        #Lyon--France,45.764043,4.835658999999964
        #Marseille--France,43.296482,5.369779999999992
        #Lille--France,50.62924999999999,3.057256000000052
        #Rennes--France,48.117266,-1.6777925999999752
        #Toulouse--France,43.604652,1.4442090000000007
        #Bordeaux--France,44.837789,-0.5791799999999512
        #Strasbourg--France,48.57340529999999,7.752111300000024
        #Nice--France,43.7101728,7.261953199999994
        #Grenoble--France,45.188529,5.724523999999974

        search_url = f"https://www.superprof.fr/s/{search_topic},{search_location_full}.html"

        self.driver.get(search_url)
        content = Selector(text=self.driver.page_source.encode('utf-8'))

        teacher_number = content.xpath("//span[@class='SearchForm_titre']/text()").get()
        teacher_number = int(re.search(r"[0-9]+",teacher_number).group(0))

        zone_offers = content.xpath("//div[@class='Search_results js-search-main-results']")
        page_offers_number = len(zone_offers.xpath(".//div[@class='AnnouncePreview  a-js tck-announce-link']"))

        pages_number = teacher_number // page_offers_number

        for page_number in range(1, 6):
            url = f'{search_url}?n={page_number}'
            yield scrapy.Request(url=url, callback=self.parse_scroller)

    def parse_scroller(self, response):
        item = SuperProfItem()

        self.driver.get(response.url)
        content = Selector(text=self.driver.page_source.encode('utf-8'))

        url = response.url

        zone_offers = content.xpath("//div[@class='Search_results js-search-main-results']")
        offers = zone_offers.xpath(".//div[@class='AnnouncePreview  a-js tck-announce-link']")

        for offer in offers:
            zone_teacher = offer.xpath(".//div[@class='AnnouncePreview_teacherName']")
            zone_picture = offer.xpath(".//div[@class='AnnouncePreview_photoWrapper']")
            zone_location = offer.xpath(".//div[@class='AnnouncePreview_location ']")
            zone_price = offer.xpath(".//div[@class='AnnouncePreview_price']")
            zone_rating = offer.xpath(".//div[@class='AnnouncePreview_rating']")
            zone_icons = offer.xpath(".//div[@class='AnnouncePreview_icons']")

            # general
            item["website"] = re.search(r"https://[A-Za-z.]*", url).group(0).split(".")[1]

            page = re.search(r"\?n=[0-9]+",url).group(0)
            item["page"] = int(page.replace("?n=", ""))
            item["search_topic"] = re.search(r"/s/[A-Za-z.]*,", url).group(0).split(",")[0].replace("/s/", "")
            item["search_location"] = url.split(",")[1]

            # teacher
            teacher_elements = zone_teacher.css('div::text').getall()
            teacher_elements = [x.strip() for x in teacher_elements]
            teacher_elements = list(filter(lambda x: True if x != "" else False, teacher_elements))
            item["teacher"] = teacher_elements[0]

            # picture
            picture = zone_picture.xpath(".//img[@class='AnnouncePreview_photo']/@src").get()
            if picture == "/images/photo-default_200.jpg":
                item["picture"] = 0
            else:
                item["picture"] = 1

            # location
            item["location"] = zone_location.css('strong::text').getall()[0]

            # price
            price_elements = zone_price.css('div::text').getall()
            price_elements = [x.strip() for x in price_elements]
            price_elements = list(filter(lambda x: True if x != "" else False, price_elements))
            item["price"] = int(re.search(r"[0-9]+", price_elements[0]).group(0))

            if offer.xpath(".//div[@class='AnnouncePreview_firstHourFree']") == []:
                item["first_free"] = 0
            else:
                item["first_free"] = 1

            # rating
            stars = {}
            stars["full"] = zone_rating.xpath(".//li[@class='Rating_star Rating_star-full']")
            stars["half"] = zone_rating.xpath(".//li[@class='Rating_star Rating_star-half']")
            item["rating"] = 1 * len(stars["full"]) + 0.5 * len(stars["half"])

            reviews_elements = zone_rating.css('div::text').getall()
            reviews_elements = [x.strip() for x in reviews_elements]
            reviews_elements = list(filter(lambda x: True if x != "" else False, reviews_elements))
            if reviews_elements == []:
                item["reviews"] = 0
            else:
                item["reviews"] = int(re.search(r"[0-9]+", reviews_elements[0]).group(0))

            # icons
            item["ambassador"] = len(zone_icons.xpath(".//i[@class='Icon Icon-trophy no-js']"))
            item["verified"] = len(zone_icons.xpath(".//i[@class='Icon Icon-check no-js']"))
            item["inperson"] = len(zone_icons.xpath(".//i[@class='Icon Icon-user no-js']"))
            item["webcam"] = len(zone_icons.xpath(".//i[@class='Icon Icon-webcam no-js']"))
            item["response_time"] = zone_icons.xpath(".//span[@class='Icon AnnouncePreview_responseTime']/text()").get()

            yield item
