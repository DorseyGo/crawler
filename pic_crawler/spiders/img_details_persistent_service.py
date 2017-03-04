#: ------------------------------------------------
#: FileName:    img_details_persistent_service.py
#: Author:  DORSEy Q F TANG
#: Date:    21 Feb 2017
#: ------------------------------------------------

from db_utils import DBManager

#: provide persistent service to the image details kind data
class ImgDetailsPersistentService():


    __INSERT_INTO_IMG_DETAILS__ = "INSERT INTO IMAGE_DETAILS(NAME, FULL_NAME, STORE_PATH, IMG_ID) VALUES (%s, %s, %s, %s)"

    def __init__(self):
        self.db_mgr = DBManager()

    #: insert the record which specified by the given parameters
    #: returns the ID last inserted or None
    def insert_and_get_id(self, name = None, full_name = None, store_path = None, img_id = None):
        if name is not None:
            params = (name, full_name, store_path, img_id)
            self.db_mgr.insertandgetid(self.__INSERT_INTO_IMG_DETAILS__, params)

        return None