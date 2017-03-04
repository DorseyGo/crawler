#: ------------------------------------------------
#: FileName:    categories_persistent_service.py
#: Author:  DORSEy Q F TANG
#: Date:    20 Feb 2017
#: ------------------------------------------------

from db_utils import DBManager

class CategoriesPersistentService():


    __FIND_ALL_AVAILABLE_CATEGORIES__ = "SELECT * FROM CATEGORIES"

    def __init__(self):
        self.db_utils = DBManager()

    def find_all_categories(self):
        return self.db_utils.queryall(self.__FIND_ALL_AVAILABLE_CATEGORIES__)