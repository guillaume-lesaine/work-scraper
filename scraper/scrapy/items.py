# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BlablaCarItem(scrapy.Item):
    website = scrapy.Field()
    travel_id = scrapy.Field()
    url = scrapy.Field()
    url_travel = scrapy.Field()
    search_date = scrapy.Field()
    search_hour = scrapy.Field()
    departure_date = scrapy.Field()
    departure_hour = scrapy.Field()
    arrival_date = scrapy.Field()
    arrival_hour = scrapy.Field()
    search_departure_city = scrapy.Field()
    search_arrival_city = scrapy.Field()
    departure_city = scrapy.Field()
    arrival_city = scrapy.Field()
    car = scrapy.Field()
    price = scrapy.Field()
    driver = scrapy.Field()
    passengers = scrapy.Field()

class LeboncoinItem(scrapy.Item):
    addition_date = scrapy.Field()
    seller = scrapy.Field()
    product = scrapy.Field()
    price = scrapy.Field()

class DrivyItem(scrapy.Item):
    owner = scrapy.Field()
    car = scrapy.Field()
    price = scrapy.Field()

class VintedItem(scrapy.Item):
    seller = scrapy.Field()
    price = scrapy.Field()

class PAPItem(scrapy.Item):
    pass

class SuperProfItem(scrapy.Item):
    website = scrapy.Field()
    page = scrapy.Field()
    search_topic = scrapy.Field()
    search_location = scrapy.Field()
    teacher = scrapy.Field()
    picture = scrapy.Field()
    location = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    reviews = scrapy.Field()
    ambassador = scrapy.Field()
    verified = scrapy.Field()
    inperson = scrapy.Field()
    webcam = scrapy.Field()
    response_time = scrapy.Field()
    first_free = scrapy.Field()
