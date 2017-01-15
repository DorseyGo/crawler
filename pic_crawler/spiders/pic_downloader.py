#: ------------------------------------------------
#: FileName:    pic_downloader.py
#: Author:  DORSEy Q F TANG
#: Date:    12 Jan 2017
#: ------------------------------------------------

import os
import urllib
from log_utils import LogUtils

class PicDownloader():
    path_to_save_img = "/Users/DORSEy/Downloads/downloads"
    #: the categories of the product
    categories = {"O": "outer", "T": "top", "D": "dress", "S": "shoes"}
    #: the name of for the logging
    name = "pic_downloader"

    #: for log
    log_utils = LogUtils()

    def determine_category(self, category):
        method_name = "determine_category()"
        logger = self.log_utils.get_log(self.name, "")

        first_catgry = category[0:1]
        existed = self.categories.has_key(first_catgry)
        if existed is False:
            logger.info("WARN - No appropriate category [%s] found", category)
            return

        return self.categories.get(first_catgry)

    def download_and_save(self, img_url, category):
        method_name = "download_and_save()"
        logger = self.log_utils.get_log(self.name, "")

        last_forward_slash_idx = img_url.rfind("/")
        question_indx = img_url.rfind("?")
        if 0 < question_indx <= last_forward_slash_idx:
            logger.warn("WARN - Illegal url addresss [%s] detected", img_url)
            return

        #: otherwise, trying to download it and save it to local file system
        file_name = img_url[last_forward_slash_idx + 1: question_indx]
        sub_folder = self.determine_category(category)
        path_to_save = self.path_to_save_img + "/" + sub_folder

        #: check if the destination folder exists
        if os.path.exists(path_to_save) is False:
            os.makedirs(path_to_save)

        dest_file = path_to_save + "/" + category + file_name
        with open(dest_file, "wb") as img:
            conn = urllib.urlopen(img_url)
            img.write(conn.read())
            img.flush()
            img.close()
            logger.info("INFO - image [%s] is writen to file [%s]", img_url, dest_file)