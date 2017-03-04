#: ------------------------------------------------
#: FileName:    pic_domains_persistent_service.py
#: Author:  DORSEy Q F TANG
#: Date:    20 Feb 2017
#: ------------------------------------------------

from db_utils import DBManager

class PicDomainsPersistentService():


    __FIND_ALL_AVAILABLE_DOMAINS__ = "SELECT DOMAIN FROM PIC_DOMAINS"

    __FIND_DOMAIN_BY_ID__ = "SELECT * FROM PIC_DOMAINS WHERE ID = %s"

    def __init__(self):
        self.db_utils = DBManager()

    def find_all_domains(self):
        return self.db_utils.queryall(self.__FIND_ALL_AVAILABLE_DOMAINS__)

    def find_domain_by_id(self, domain_id = None):
        if domain_id is not None:
            params = (domain_id, )
            return self.db_utils.queryone(self.__FIND_DOMAIN_BY_ID__, params)

        return None