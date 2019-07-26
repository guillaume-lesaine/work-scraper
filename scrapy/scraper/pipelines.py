# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter
from scrapy.exceptions import DropItem
import time
import re

class TreatmentPipeline(object):

    def process_item(self, item, spider):
        website = item["website"]
        if website == "blablacar":
            url = item["url"]
            url_travel = item["url_travel"]
            result = re.search(r"/[0-9]*-", url_travel).group(0)
            travel_id = re.search(r"[0-9]+", result).group(0)
            item["travel_id"] = travel_id
            item["search_departure_city"] = re.search(r"formatted_from=[A-Za-z]*", url).group(0).replace("formatted_from=","")
            item["search_arrival_city"] = re.search(r"formatted_to=[A-Za-z]*", url).group(0).replace("formatted_to=","")
        if website == "superprof":
            pass
        return item

class JsonLinesExportPipeline(object):

    def open_spider(self, spider):
        self.unit_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.unit_to_exporter.values():
            exporter.finish_exporting()
            exporter.file.close()

    def _exporter_for_item(self, item):
        website = item["website"]

        unit = ""

        if website == "blablacar":
            search_departure_city = item["search_departure_city"]
            search_arrival_city = item["search_arrival_city"]
            unit = "-".join([search_departure_city, search_arrival_city])
            search_date = item["search_date"]
            search_hour = item["search_hour"]
            full_search_date = "-".join([search_date,search_hour])
            full_current_date = time.strftime("%Y-%m-%d-%Hh-%Mm-%Ss")

            export_name = f'{website}_departure={search_departure_city}_arrival={search_arrival_city}_scraping-date={full_current_date}_travel-date={full_search_date}.json'

        if website == "superprof":
            search_topic = item["search_topic"]
            search_location = item["search_location"]
            teacher = item["teacher"]

            full_current_date = time.strftime("%Y-%m-%d-%Hh-%Mm-%Ss")

            export_name = f'{search_topic}_{full_current_date}_{search_location.lower()}.json'

        if unit not in self.unit_to_exporter:
            f = open(f"./outputs_{website}/{export_name}", 'wb')
            exporter = JsonLinesItemExporter(f)
            exporter.start_exporting()
            self.unit_to_exporter[unit] = exporter

        return self.unit_to_exporter[unit]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item
