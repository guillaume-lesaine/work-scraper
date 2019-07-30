import scrapy
from scraper.items import BlablaCarItem
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.utils.log import configure_logging  
import logging 
import time
from datetime import datetime, timedelta
import re
import json

class BlablaCarSpider(scrapy.Spider):
    name = "blablacar"
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.ERROR
    )

    def __init__(self):
        pass

    def start_requests(self):
        urls = []
        urls_xhr = []
        search_dates_repetition = []

        current_date = datetime.now()
        search_dates = [current_date + timedelta(days=i) for i in range(1,2)]
        search_dates = map(lambda d : datetime.strftime(d, "%Y-%m-%d"), search_dates)

        search_hour = "08"

        for search_date in search_dates:

            unit_urls = [
                f"https://www.blablacar.fr/search?fn=Paris%2C%20France&fc=48.856614%2C2.352221&fcc=FR&formatted_from=Paris&tn=Marseille%2C%20France&tc=43.296482%2C5.36978&tcc=FR&formatted_to=Marseille&db={search_date}&hb={search_hour}&departure_location_id=eyJpIjoiQ2hJSkQ3ZmlCaDl1NWtjUllKU01hTU9DQ3dRIiwicCI6MSwidiI6MSwidCI6W119&arrival_location_id=eyJpIjoiQ2hJSk0xUGFSRU9feVJJUklBS1hfYVVaQ0FRIiwicCI6MSwidiI6MSwidCI6W119&departure_city=Paris&arrival_city=Marseille&searchOrigin=search",
                # f"https://www.blablacar.fr/search?fn=Paris%2C%20France&fc=48.856614%2C2.352221&fcc=FR&formatted_from=Paris&tn=Strasbourg%2C%20France&tc=48.573405%2C7.752111&tcc=FR&formatted_to=Strasbourg&db={search_date}&hb={search_hour}&departure_location_id=eyJpIjoiQ2hJSkQ3ZmlCaDl1NWtjUllKU01hTU9DQ3dRIiwicCI6MSwidiI6MSwidCI6W119&arrival_location_id=eyJpIjoiQ2hJSndiSVlYa25JbGtjUkh5VG5HREZJR3BjIiwicCI6MSwidiI6MSwidCI6W119&departure_city=Paris&arrival_city=Strasbourg&searchOrigin=search",
                # f"https://www.blablacar.fr/search?fn=Paris%2C%20France&fc=48.856614%2C2.352221&fcc=FR&formatted_from=Paris&tn=Lille%2C%20France&tc=50.62925%2C3.057256&tcc=FR&formatted_to=Lille&db={search_date}&hb={search_hour}&departure_location_id=eyJpIjoiQ2hJSkQ3ZmlCaDl1NWtjUllKU01hTU9DQ3dRIiwicCI6MSwidiI6MSwidCI6W119&arrival_location_id=eyJpIjoiQ2hJSkVXNGxzM25Wd2tjUllHTmtnVDd4Q2dRIiwicCI6MSwidiI6MSwidCI6W119&departure_city=Paris&arrival_city=Lille&searchOrigin=search",
                # f"https://www.blablacar.fr/search?fn=Paris%2C%20France&fc=48.856614%2C2.352221&fcc=FR&formatted_from=Paris&tn=Rennes%2C%20France&tc=48.117266%2C-1.677792&tcc=FR&formatted_to=Rennes&db={search_date}&hb={search_hour}&departure_location_id=eyJpIjoiQ2hJSkQ3ZmlCaDl1NWtjUllKU01hTU9DQ3dRIiwicCI6MSwidiI6MSwidCI6W119&arrival_location_id=eyJpIjoiQ2hJSmhaRFdweV9lRGtnUk1LdmtOczJsREFRIiwicCI6MSwidiI6MSwidCI6W119&departure_city=Paris&arrival_city=Rennes&searchOrigin=search",
                # f"https://www.blablacar.fr/search?fn=Paris%2C%20France&fc=48.856614%2C2.352221&fcc=FR&formatted_from=Paris&tn=Bordeaux%2C%20France&tc=44.837789%2C-0.57918&tcc=FR&formatted_to=Bordeaux&db={search_date}&hb={search_hour}&departure_location_id=eyJpIjoiQ2hJSkQ3ZmlCaDl1NWtjUllKU01hTU9DQ3dRIiwicCI6MSwidiI6MSwidCI6W119&arrival_location_id=eyJpIjoiQ2hJSmdjcFI5LWduVlEwUmlYbzVld09HWTNrIiwicCI6MSwidiI6MSwidCI6W119&departure_city=Paris&arrival_city=Bordeaux&searchOrigin=search"
            ]

            unit_urls_xhr = [
                lambda x :f"https://edge.blablacar.com/trips/search?departure_address=Paris%2C%20France&departure_coordinates=48.856614%2C2.352221&departure_city=Paris&departure_country_code=FR&arrival_coordinates=43.296482%2C5.36978&arrival_address=Marseille%2C%20France&arrival_city=Marseille&arrival_country_code=FR&date_begin={search_date}T{search_hour}:00:00&page={x}&search_tracktor_uuid=e87445e6-9879-4a0f-b3a2-df5e7b4f0df4",
                # lambda x :f"https://edge.blablacar.com/trips/search?departure_address=Paris%2C%20France&departure_coordinates=48.856614%2C2.352221&departure_city=Paris&departure_country_code=FR&arrival_coordinates=48.573405%2C7.752111&arrival_address=Strasbourg%2C%20France&arrival_city=Strasbourg&arrival_country_code=FR&date_begin={search_date}T{search_hour}:00:00&page={x}&search_tracktor_uuid=6581e86d-a199-48b0-8302-096eef3cf1e4",
                # lambda x: f"https://edge.blablacar.com/trips/search?departure_address=Paris%2C%20France&departure_coordinates=48.856614%2C2.352221&departure_city=Paris&departure_country_code=FR&arrival_coordinates=50.62925%2C3.057256&arrival_address=Lille%2C%20France&arrival_city=Lille&arrival_country_code=FR&date_begin={search_date}T{search_hour}:00:00&page={x}&search_tracktor_uuid=92eab4bc-a44a-4f46-8feb-53ebf9cb4f3b",
                # lambda x: f"https://edge.blablacar.com/trips/search?departure_address=Paris%2C%20France&departure_coordinates=48.856614%2C2.352221&departure_city=Paris&departure_country_code=FR&arrival_coordinates=48.117266%2C-1.677792&arrival_address=Rennes%2C%20France&arrival_city=Rennes&arrival_country_code=FR&date_begin={search_date}T{search_hour}:00:00&page={x}&search_tracktor_uuid=4b6c30a2-7dce-4a8e-bf11-4b44914c07f6",
                # lambda x: f"https://edge.blablacar.com/trips/search?departure_address=Paris%2C%20France&departure_coordinates=48.856614%2C2.352221&departure_city=Paris&departure_country_code=FR&arrival_coordinates=44.837789%2C-0.57918&arrival_address=Bordeaux%2C%20France&arrival_city=Bordeaux&arrival_country_code=FR&date_begin={search_date}T{search_hour}:00:00&page={x}&search_tracktor_uuid=c4e71aaf-2354-4cd5-acda-ef535076819c"
            ]

            urls += unit_urls
            urls_xhr += unit_urls_xhr

            search_dates_repetition += [search_date for i in range(len(unit_urls))]

        for url, url_xhr, search_date in zip(urls, urls_xhr, search_dates_repetition):
            yield scrapy.Request(url=url, callback=self.parse_scroller, errback=self.connection_error, meta={"url": url, "url_xhr":url_xhr, "search_date": search_date, "search_hour": search_hour})

    def connection_error(self, failure):
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('----- Headers %s', response.headers)
            self.logger.error('----- Body %s', response.body)
            self.logger.error('----- Request %s', response.request.headers)
            self.logger.error('----- Cookies request %s', response.request.headers.getlist('Cookie'))
            self.logger.error('----- Cookies response %s', response.headers.getlist('Set-Cookie'))

    def parse_scroller(self, response):
        zone_information = response.xpath("//div[@class='filtersBar flex fixed large:static']")
        number_offers = zone_information.css('h1::text').getall()[0]
        number_offers = int(re.search(r"[0-9]*", number_offers).group(0))

        number_request = number_offers // 10 + 1

        url = response.meta["url"]
        search_date = response.meta["search_date"]
        search_hour = response.meta["search_hour"]

        for page in range(1, number_request + 1):
            url_xhr = response.meta["url_xhr"]
            url_xhr = url_xhr(page)

            yield scrapy.http.Request(
                url = url_xhr,
                method = "GET",
                headers = {
                    "Host": "edge.blablacar.com",
                    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/47.0',
                    "Accept": "application/json",
                    "Accept-Language": "fr_FR",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Referer": url,
                    "Content-Type": "application/json",
                    "x-locale": "fr_FR",
                    "x-visitor-id": "ztaMPyyAahdR8+isOsWbfA==",
                    "x-currency": "EUR",
                    "x-correlation-id": "f99424f7-1e40-4220-b0e4-a3aa68ac758d",
                    "x-client": "SPA|1.0.0",
                    "x-forwarded-proto": "https",
                    "Authorization": "Bearer 805a09bb-7669-4aba-8e52-8d1058d0cb26",
                    "Origin": "https://www.blablacar.fr",
                    "Connection": "keep-alive",
                    "TE": "Trailers",
                    "Upgrade-Insecure-Requests": "1",
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache",
                },
                callback=self.parse_json,
                meta=response.meta
            )

    def parse_json(self, response):
        trips = json.loads(response.body)["trips"]

        for trip in trips:
            meta = response.meta
            search_date = meta["search_date"]
            search_date = datetime.strptime(search_date, "%Y-%m-%d")

            departure_date = trip["waypoints"][0]["departure_date"]
            departure_date = datetime.strptime(departure_date, "%Y-%m-%dT%H:%M:%S")
            departure_date = datetime.strftime(departure_date, "%Y-%m-%d")
            departure_date = datetime.strptime(departure_date, "%Y-%m-%d")

            arrival_date = trip["waypoints"][1]["departure_date"]
            arrival_date = datetime.strptime(arrival_date, "%Y-%m-%dT%H:%M:%S")
            arrival_date = datetime.strftime(arrival_date, "%Y-%m-%d")
            arrival_date = datetime.strptime(arrival_date, "%Y-%m-%d")

            href = trip["multimodal_id"]["id"]

            if departure_date > search_date:
                pass
            else:
                url_details = f"https://www.blablacar.fr/trip/carpooling/{href}"
                departure_date = datetime.strftime(departure_date, "%Y-%m-%d")
                arrival_date = datetime.strftime(arrival_date, "%Y-%m-%d")
                meta["url_travel"] = url_details
                meta["departure_date"] = departure_date
                meta["arrival_date"] = arrival_date

                yield scrapy.Request(url_details, callback=self.parse_details, meta=meta)

    def parse_details(self, response):
        item = BlablaCarItem()

        url = response.meta["url"]
        item["url"] = url
        item["website"] = re.search(r"https://[A-Za-z.]*", url).group(0).split(".")[1]
        item["url_travel"] = response.meta["url_travel"]
        item["search_date"] = response.meta["search_date"]
        hour = datetime.strptime(response.meta["search_hour"], "%H")
        item["search_hour"] = datetime.strftime(hour, "%Hh-%Mm-%Ss")
        item["departure_date"] = response.meta["departure_date"]
        item["arrival_date"] = response.meta["arrival_date"]

        # Date
        zone_dates = response.xpath("//time[@class='jsx-1448366035']")
        dates_flags = [t.xpath(".//span[@class='kirk-text kirk-text-titleStrong']/text()").get() for t in zone_dates]
        item["departure_hour"], item["arrival_hour"] = tuple(dates_flags)

        # Cities
        zone_cities = response.xpath("//ul[@class='jsx-1448366035 py-xl']")
        cities_flags = zone_cities.xpath(".//p[@class='kirk-text kirk-text-body']/text()").getall()
        item["departure_city"], item["arrival_city"] = tuple(cities_flags)

        # Price
        zone_price = response.xpath("//div[@class='kirk-text kirk-text-subheaderStrong']")
        price = zone_price.xpath(".//div/text()").get()
        item["price"] = price

        # Car
        zone_car = response.xpath("//section[@class='py-l u-separator-top']")
        car = zone_car.xpath(".//div[@class='kirk-text kirk-text-title kirk-item-title']/text()").get()
        item["car"] = car

        # Travel preferences
        zone_travel_preferences = zone_car.xpath(".//div[@class='jsx-1542968643 kirk-item-leftText']")
        item["travel_preferences"] = zone_travel_preferences.xpath(".//div[@class='kirk-text kirk-text-body kirk-item-body']/text()").getall()

        # Driver
        driver_url = response.xpath("//a[@class='jsx-1542968643 kirk-item kirk-item--clickable kirk-item-choice']").attrib['href']
        driver_url = response.urljoin(driver_url)

        # Passengers
        item["passengers"] = []

        passenger_selectors = response.xpath("//a[@class='jsx-1542968643 kirk-item kirk-item--clickable']")
        passenger_urls = [response.urljoin(passenger.attrib['href']) for passenger in passenger_selectors]
        passenger_urls_generator = (x for x in passenger_urls)

        try:
            passenger_url = next(passenger_urls_generator)
            meta = {"item": item, "driver_url": driver_url,"passenger_urls_generator":passenger_urls_generator}
            yield scrapy.Request(passenger_url, callback=self.get_personal_details_passenger, meta=meta)
        except:
            meta = {"item": item}
            yield scrapy.Request(driver_url, callback=self.get_personal_details_driver, meta=meta)

    def get_personal_details_driver(self, response):
        item = response.meta['item']
        name = response.xpath("//h1[@class='kirk-title my-l']/text()").get()
        age = response.xpath("//p[@class='kirk-text kirk-text-body']/text()").get()

        item["driver"]={"name": name, "age":age}

        yield item

    def get_personal_details_passenger(self, response):
        item = response.meta["item"]
        driver_url = response.meta["driver_url"]
        passenger_urls_generator = response.meta["passenger_urls_generator"]

        name = response.xpath("//h1[@class='kirk-title my-l']/text()").get()
        age = response.xpath("//p[@class='kirk-text kirk-text-body']/text()").get()

        item["passengers"].append({"name": name, "age":age})

        try:
            passenger_url = next(passenger_urls_generator)
            meta = {"item": item, "driver_url": driver_url,"passenger_urls_generator":passenger_urls_generator}
            yield scrapy.Request(passenger_url, callback=self.get_personal_details_passenger, meta=meta)
        except:
            meta = {"item": item}
            yield scrapy.Request(driver_url, callback=self.get_personal_details_driver, meta=meta)