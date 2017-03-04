#: ------------------------------------------------
#: FileName:    images_persistent_service.py
#: Author:  DORSEy Q F TANG
#: Date:    20 Feb 2017
#: ------------------------------------------------

from db_utils import DBManager

#: provide persistent service to images
class ImagesPersistentService():


    __FIND_IMG_BY_NAME__ = "SELECT * FROM IMAGES WHERE NAME = %s"

    __INSERT_INTO_ONE_IMG__ = "INSERT INTO IMAGES(NAME, FULL_NAME, STORE_PATH, CATEGORY_ID, DOMAIN_ID) VALUES (%s, %s, %s, %s, %s)"

    __FIND_IMG_BY_CONDITION__ = "SELECT * FROM IMAGES WHERE NAME = %s AND DOMAIN_ID = %s AND CATEGORY_ID = %s"

    def __init__(self):
        self.db_utils = DBManager()

    #: find images by its name provided
    #: returns None if no corresponding image found
    def find_img_by_name(self, name = None):
        if name is not None:
            params = (name, )
            return self.db_utils.queryone(self.__FIND_IMG_BY_NAME__, params)

        return None

    #: add the image with property specified, and return the id
    #: false if the return value is None
    def insert_and_get_id(self, name = None, full_name = None, store_path = None, category_id = None, domain_id = None):
        if name is not None:
            params = (name, full_name, store_path, category_id, domain_id)
            return self.db_utils.insertandgetid(self.__INSERT_INTO_ONE_IMG__, params)

        return None

    def is_img_exists(self, img_name, domain_id, category_id):
        if img_name is not None:
            params = (img_name, domain_id, category_id)
            result = self.db_utils.queryone(self.__FIND_IMG_BY_CONDITION__, params)

            if result is not None:
                return True

        return False

if __name__ == '__main__':
    img_service = ImagesPersistentService()
    result = img_service.is_img_exists('O0030020001303', 1, 3)
    print str(result)