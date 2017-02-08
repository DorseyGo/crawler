#: ------------------------------------------------
#: FileName:    pic_downloader.py
#: Author:  DORSEy Q F TANG
#: Date:    12 Jan 2017
#: ------------------------------------------------

import os
import urllib
from log_utils import LogUtils
from configs import Configs
from db_utils import DBManager

class PicDownloader():


    #: the name of for the logging
    name = "pic_downloader"
    pic_categories = {}
    category_id_abbrevs = {}

    #: for log
    log_utils = LogUtils()
    cnf = Configs()
    db_mgr = DBManager()

    #: SQL statement
    __select_all_categories_stmt = "SELECT ID, ABBREVIATION, CATEGORY FROM CATEGORIES"
    __insert_into_images = "INSERT INTO IMAGES(NAME, FULL_NAME, STORE_PATH, CATEGORY_ID) VALUES(%s, %s, %s, %s)"

    def __init__(self):
        self.path_to_save_img = self.cnf.sysconf("sys_pic_save_path")
        categories = self.db_mgr.queryall(self.__select_all_categories_stmt)
        for category in categories:
            self.pic_categories[category['ABBREVIATION']] = category['CATEGORY']
            self.category_id_abbrevs[category['ABBREVIATION']] = category['ID']

        print str(self.pic_categories)

    def determine_category(self, category):
        logger = self.log_utils.get_log(self.name, "")

        first_catgry = category[0:1]
        existed = self.pic_categories.has_key(first_catgry)
        if existed is False:
            logger.info("WARN - No appropriate category [%s] found", category)
            return

        return self.pic_categories.get(first_catgry)

    def download_and_save(self, img_url, category):
        logger = self.log_utils.get_log(self.name, "")

        last_forward_slash_idx = img_url.rfind("/")
        question_indx = img_url.rfind("?")

        #: otherwise, trying to download it and save it to local file system
        if question_indx < 0:
            file_name = img_url[last_forward_slash_idx + 1: ]
        else:
            file_name = img_url[last_forward_slash_idx + 1: question_indx]

        sub_folder = self.determine_category(category)
        path_to_save = self.path_to_save_img + "/" + sub_folder

        #: check if the destination folder exists
        if os.path.exists(path_to_save) is False:
            os.makedirs(path_to_save)

        saved_file_name = category + file_name
        dest_file = path_to_save + "/" + saved_file_name
        with open(dest_file, "wb") as img:
            conn = urllib.urlopen(img_url)
            img.write(conn.read())
            img.flush()
            img.close()
            logger.info("INFO - image [%s] is writen to file [%s]", img_url, dest_file)

        #: after save it to local file system, persistent the data to underlying database
        params = (saved_file_name, saved_file_name, path_to_save, self.category_id_abbrevs.get(category))
        self.db_mgr.insertandgetid(self.__insert_into_images, params)