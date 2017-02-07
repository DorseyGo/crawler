#: ------------------------------------------------
#: FileName:    pic_crawler.py
#: Author:  DORSEy Q F TANG
#: Date:    12 Jan 2017
#: ------------------------------------------------

import scrapy
from pic_downloader import PicDownloader
from log_utils import LogUtils
from db_utils import DBManager

#: crawl down all the desired images from the url address specified
class PicCrawler(scrapy.Spider):


    name = "pic"
    #: start_urls = ['http://www.roer.co.kr/shop/shopbrand.html?xcode=003&type=X']
    allowed_domain = "http://www.roer.co.kr"

    #: register the downloader and file persistence
    pic_downloader = PicDownloader()
    HTTP_PRO = "http"

    #: log utils
    log_utils = LogUtils()

    #: instance of database manager
    db_mgr = DBManager()

    #: SQL statements
    __select_all_src_urls_stmt = "SELECT URL_ADDR FROM PIC_CATEGORIES_2_URL"
    __select_category_and_rule_stmt = "SELECT c.ABBREVIATION, pd.RULE_4_NAVI_IMG FROM PIC_CATEGORIES_2_URL pc2u \
                                          LEFT JOIN CATEGORIES c ON pc2u.CATEGORY_ID = c.ID \
                                        LEFT JOIN PIC_DOMAINS pd ON pc2u.DOMAIN_ID = pd.ID \
                                      WHERE pc2u.URL_ADDR = %s"

    def start_requests(self):
        url_addrs = self.db_mgr.queryall(self.__select_all_src_urls_stmt)
        for url_addr in url_addrs:
            yield self.make_requests_from_url(url_addr['URL_ADDR'])

    def join_url_if_needed(self, response, image_url):
        if image_url.startswith(self.HTTP_PRO):
            img_url = image_url
        else:
            img_url = response.urljoin(image_url)

        return img_url

    def parse(self, response):
        logger = self.log_utils.get_log(self.name, "")
        logger.debug("DEBUG - parsing response from url [%s]", response.url)

        params = (response.url, )
        rules_2_navigate_2_img = self.db_mgr.queryone(self.__select_category_and_rule_stmt, params)
        image_urls = response.xpath(rules_2_navigate_2_img['RULE_4_NAVI_IMG']).extract()

        #: iterate over the image urls
        for image_url in image_urls:
            logger.info("INFO - Image URL address [%s] detected", image_url)

            img_url = self.join_url_if_needed(response, image_url)
            #: download and persistent it to local file system
            self.pic_downloader.download_and_save(img_url, rules_2_navigate_2_img['ABBREVIATION'])

        #: trying to load the next pages link
        next_page = response.xpath("//a[@class='now']").xpath("..").xpath("./following-sibling::*").xpath("./li/a/@href").extract_first()
        if next_page:
            logger.info("INFO - Navigate to the next page [%s] to crawl desired data", next_page)
            next_link = self.join_url_if_needed(response, next_page)
            yield scrapy.Request(next_link, callback = self.parse)