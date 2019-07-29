import scrapy
from scrapy.crawler import CrawlerProcess
import scraper.spiders as spd

spider = spd.BlablaCarSpider

process = CrawlerProcess(settings={
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'ROBOTSTXT_OBEY':False,
    'CONCURRENT_REQUESTS': 1,
    'DOWNLOAD_DELAY': 10,
    'COOKIES_ENABLED': False,
    'ITEM_PIPELINES': {
        'scraper.pipelines.TreatmentPipeline': 200,
        'scraper.pipelines.JsonLinesExportPipeline': 300,
    }
})

process.crawl(spider)
process.start()