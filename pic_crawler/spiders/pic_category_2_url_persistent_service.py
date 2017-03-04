#: ------------------------------------------------
#: FileName:    pic_category_2_url_persistent_service.py
#: Author:  DORSEy Q F TANG
#: Date:    20 Feb 2017
#: ------------------------------------------------

from db_utils import DBManager

#: provide persistent service to its invoker
class PicCategory2UrlPersistentService():

    __FIND_ALL_SRC_URLS__ = "SELECT URL_ADDR FROM PIC_CATEGORIES_2_URL"

    #: SQL statements to grab all available url address to crawl the desired images.
    __FIND_CATEGORY_AND_RULE_BY_URL_ADDR__ = "SELECT c.ABBREVIATION, pd.ID DOMAIN_ID, pd.RULE_4_NAVI_IMG, pd.RULE_4_LOCATE_DETAIL_IMG, pd.RULE_4_NAVI_2_NEXT_PAGE,\
                                            pd.PATTERN_EXTRACT_PAGINATION FROM PIC_CATEGORIES_2_URL pc2u \
                                          LEFT JOIN CATEGORIES c ON pc2u.CATEGORY_ID = c.ID \
                                        LEFT JOIN PIC_DOMAINS pd ON pc2u.DOMAIN_ID = pd.ID \
                                      WHERE pc2u.URL_ADDR = %s AND pd.ENABLE = 0"

    def __init__(self):
        self.db_utils = DBManager()

    #: find all available url address
    def find_all_src_urls(self):
        return self.db_utils.queryall(self.__FIND_ALL_SRC_URLS__)

    #: query the category and rules for navigating the images by url address
    def find_category_and_rule_by_src_url(self, url_addr = None):
        if url_addr is not None:
            params = (url_addr, )
            return self.db_utils.queryone(self.__FIND_CATEGORY_AND_RULE_BY_URL_ADDR__, params)

        return None

if __name__ == '__main__':
    service = PicCategory2UrlPersistentService()
    url_addr = 'http://www.roer.co.kr/shop/shopbrand.html?xcode=003&type=X'
    result = service.find_category_and_rule_by_src_url(url_addr)
    print str(result)