#: ------------------------------------------------
#: FileName:    pic_crawler.py
#: Author:  DORSEy Q F TANG
#: Date:    12 Jan 2017
#: ------------------------------------------------

import scrapy
from pic_downloader import PicDownloader
from log_utils import LogUtils

# crawl down all the desired images from the url address specified
class PicCrawler(scrapy.Spider):
    name = "pic"
    start_urls = ['http://www.roer.co.kr/shop/shopbrand.html?xcode=003&type=X']
    allowed_domain = "http://www.roer.co.kr"

    #: register the downloader and file persistence
    pic_downloader = PicDownloader()
    HTTP_PRO = "http"

    #: log utils
    log_utils = LogUtils()

    def join_url_if_needed(self, response, image_url):
        img_url = ""
        if image_url.startswith(self.HTTP_PRO):
            img_url = image_url
        else:
            img_url = response.urljoin(image_url)

        return img_url

    def parse(self, response):
        logger = self.log_utils.get_log(self.name, "")

        image_urls = response.xpath("//img[@class='MS_prod_img_s']/@src").extract()

        #: iterate over the image urls
        img_url = ''
        for image_url in image_urls:
            logger.info("INFO - Image URL address [%s] detected", image_url)

            img_url = self.join_url_if_needed(response, image_url)

            #: download and persistent it to local file system
            self.pic_downloader.download_and_save(img_url, "O")

        #: trying to load the next pages link
        next_page = response.xpath("//a[@class='now']").xpath("..").xpath("./following-sibling::*").xpath("./li/a/@href").extract_first()
        if next_page:
            logger.info("INFO - Navigate to the next page [%s] to crawl desired data", next_page)
            next_link = self.join_url_if_needed(response, next_page)
            yield scrapy.Request(next_link, callback = self.parse)