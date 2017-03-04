#: ------------------------------------------------
#: FileName:    pic_crawler.py
#: Author:  DORSEy Q F TANG
#: Date:    12 Jan 2017
#: ------------------------------------------------

import scrapy
import re
import time
from pic_downloader import PicDownloader
from log_utils import LogUtils
from configs import Configs
from pic_domains_persistent_service import PicDomainsPersistentService
from pic_category_2_url_persistent_service import PicCategory2UrlPersistentService

#: crawl down all the desired images from the url address specified
class PicCrawler(scrapy.Spider):


    name = "pic"
    #: start_urls = ['http://www.roer.co.kr/shop/shopbrand.html?xcode=003&type=X']
    allowed_domain = []

    #: register the downloader and file persistence
    pic_downloader = PicDownloader()
    HTTP_PRO = "http"

    def __init__(self):
        self.log_utils = LogUtils();

        self.depth_navi_next_link = int(Configs().sysconf("depth_2_next_page"))

        self.domain_persistent_service = PicDomainsPersistentService()
        self.pic_categry_2_url_persistent_service = PicCategory2UrlPersistentService()

        domains = self.domain_persistent_service.find_all_domains()
        for domain in domains:
            self.allowed_domain.append(domain['DOMAIN'])

    def start_requests(self):
        url_addrs = self.pic_categry_2_url_persistent_service.find_all_src_urls()
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

        rules_2_navigate_2_img = self.pic_categry_2_url_persistent_service.find_category_and_rule_by_src_url(response.url)
        print str(rules_2_navigate_2_img)
        rule_4_navi_img = rules_2_navigate_2_img['RULE_4_NAVI_IMG']
        rule_4_navi_next_link = rules_2_navigate_2_img['RULE_4_NAVI_2_NEXT_PAGE']
        rul2_2_locate_detail_img = rules_2_navigate_2_img['RULE_4_LOCATE_DETAIL_IMG']
        category_abbreviation = rules_2_navigate_2_img['ABBREVIATION']
        domain_id = rules_2_navigate_2_img['DOMAIN_ID']
        pattern_2_extract_pagination = rules_2_navigate_2_img['PATTERN_EXTRACT_PAGINATION']

        #: compile the pattern
        pattern = re.compile(pattern_2_extract_pagination)

        logger.debug("DEBUG - locate image rule[%s], locate detail images rule[%s], category[%s]",rule_4_navi_img, rul2_2_locate_detail_img, category_abbreviation)
        yield scrapy.Request(response.url, callback=self.parse_detail,
                             meta={"RULE_2_LOCATE_IMG": rule_4_navi_img, "CATEGORY": category_abbreviation, "DOMAIN_ID": domain_id, "RULE_2_LOCATE_DETAIL_IMG": rul2_2_locate_detail_img})

        #: goto next page if available
        self.navigate_2_next_page(response, rule_4_navi_next_link, pattern, rule_4_navi_img, category_abbreviation, domain_id=domain_id, rule_2_locate_detail_img=rul2_2_locate_detail_img)

        #: sleep for a little while
        time.sleep(10)

    def parse_detail(self, response):
        logger = self.log_utils.get_log(self.name, "")
        rule_2_locate_img = response.meta['RULE_2_LOCATE_IMG']
        category_abbrev = response.meta['CATEGORY']
        domain_id = response.meta['DOMAIN_ID']
        rule_2_locate_detail_img = response.meta['RULE_2_LOCATE_DETAIL_IMG']

        logger.debug("DEBUG - grab images from url address -->>>[%s]<<<--", response.url)

        img_elems = response.xpath(rule_2_locate_img)
        for img_elem in img_elems:
            #: fetch the entrance image
            image_url = img_elem.xpath('.//@src').extract_first()
            img_url = self.join_url_if_needed(response, image_url)
            parent_img_id = self.pic_downloader.download_and_save(img_url=img_url, category=category_abbrev, domain_id=domain_id)
            #: fetch the detail images
            detail_img_url = img_elem.xpath('..').xpath('.//@href').extract_first()
            detail_img_url = self.join_url_if_needed(response, detail_img_url)
            yield scrapy.Request(detail_img_url, callback=self.parse_link_of, meta={"RULE_2_LOCATE_IMG": rule_2_locate_detail_img, "CATEGORY": category_abbrev, "DOMAIN_ID": domain_id, "PARENT_IMG_ID": parent_img_id})

    #: parsing the link of the image grabbed, this is for getting detail images of the
    #: specific image
    def parse_link_of(self, response):
        logger = self.log_utils.get_log(self.name)
        logger.debug("DEBUG ------------>>>>> Parsing the image detail of <<<<------------- %s", response.url)
        rule_2_locate_img = response.meta['RULE_2_LOCATE_IMG']
        category_abbrev = response.meta['CATEGORY']
        domain_id = response.meta['DOMAIN_ID']
        parent_img_id = response.meta['PARENT_IMG_ID']

        logger.debug("DEBUG - ----->>>>>>>>>>>>parent_img_id = %s", parent_img_id)

        detail_img_urls = response.xpath(rule_2_locate_img).xpath('.//@src').extract()
        if detail_img_urls:
            for detail_img_url in detail_img_urls:
                img_url = self.join_url_if_needed(response, detail_img_url)
                self.pic_downloader.download_and_save(img_url=img_url, category=category_abbrev, domain_id = domain_id, parent_img_id=parent_img_id)

    #: navigate to the next page if pagination enabled in current website
    def navigate_2_next_page(self, response, rule_2_navi_next_link, pattern, rule_4_navi_img, category, domain_id, rule_2_locate_detail_img):
        logger = self.log_utils.get_log(self.name, "")
        if rule_2_navi_next_link:
            cur_page_link = response.xpath(rule_2_navi_next_link)
            match = pattern.search(cur_page_link)
            if match:
                pagination = match.group()
                #: split the kind page=1 to page=
                equal_idx = pagination.rfind("=")
                equal_symbol_with_left = pagination[0: equal_idx + 1]

                offset = 1
                #: first one already crawled
                page_num = 1
                while offset < self.depth_navi_next_link:
                    page_num = page_num + offset
                    newest_page = equal_symbol_with_left + page_num
                    rule_2_navi_next_link = rule_2_navi_next_link.replace(pagination, newest_page)
                    logger.debug("DEBUG - Navigate to next link with url segment [%s]", rule_2_navi_next_link)
                    next_link = self.join_url_if_needed(rule_2_navi_next_link)
                    yield scrapy.Request(next_link, callback=self.parse_detail, meta={"RULE_2_LOCATE_IMG": rule_4_navi_img, "CATEGORY": category, "DOMAIN_ID": domain_id, "RULE_2_LOCATE_DETAIL_IMG": rule_2_locate_detail_img})
                    #: increase 1
                    offset += 1
