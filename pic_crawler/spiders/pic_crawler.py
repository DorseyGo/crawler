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
        logger.debug("DEBUG - parsing response FROM URL ADDRESS --->>> [%s]", response.url)

        params = (response.url, )
        rules_2_navigate_2_img = self.db_mgr.queryone(self.__select_category_and_rule_stmt, params)
        rule_4_navi_img = rules_2_navigate_2_img['RULE_4_NAVI_IMG']
        category_abbreviation = rules_2_navigate_2_img['ABBREVIATION']

        logger.debug("Attempt to using rule [%s] to locate image and it belongs to category [%s]", rule_4_navi_img, category_abbreviation)
        yield scrapy.Request(response.url, callback=self.parse_detail, meta={"rule_2_locate_img": rule_4_navi_img, "category": category_abbreviation})

    def parse_detail(self, response):
        rule_2_locate_img = response.meta['rule_2_locate_img']
        category_abbrev = response.meta['category']

        logger = self.log_utils.get_log(self.name, "")
        logger.debug("DEBUG - grab images from url address -->>>[%s]<<<--", response.url)

        image_urls = response.xpath(rule_2_locate_img).extract()
        for image_url in image_urls:
            img_url = self.join_url_if_needed(response, image_url)
            self.pic_downloader.download_and_save(img_url, category_abbrev)

        #: navigate to next page
        next_page = response.xpath("//a[@class='now']").xpath("..").xpath("./following-sibling::*").xpath("./li/a/@href").extract_first()
        if next_page:
            next_link = self.join_url_if_needed(response, next_page)
            logger.debug("DEBUG - Navigate to next page -->>>[%s]", next_link)
            yield scrapy.Request(next_link, callback=self.parse_detail, meta={"rule_2_locate_img": rule_2_locate_img, "category": category_abbrev})