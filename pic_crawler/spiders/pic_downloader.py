#: ------------------------------------------------
#: FileName:    pic_downloader.py
#: Author:  DORSEy Q F TANG
#: Date:    12 Jan 2017
#: ------------------------------------------------

import os
import urllib
from log_utils import LogUtils
from configs import Configs
from images_persistent_service import ImagesPersistentService
from pic_domains_persistent_service import PicDomainsPersistentService
from categories_persistent_service import CategoriesPersistentService
from img_details_persistent_service import ImgDetailsPersistentService

#: used to download the picture from the url address given, and
#: store this kind of information into the underlying database.
class PicDownloader():


    #: the name of for the logging
    name = "pic_downloader"
    pic_categories = {}
    category_id_abbrevs = {}

    #: for log
    log_utils = LogUtils()
    cnf = Configs()


    def __init__(self):
        self.image_persistent_service = ImagesPersistentService()
        self.image_detail_persistent_service = ImgDetailsPersistentService()
        self.domain_persistent_service = PicDomainsPersistentService()
        self.categories_persistent_service = CategoriesPersistentService()
        self.path_to_save_img = self.cnf.sysconf("sys_pic_save_path")
        categories = self.categories_persistent_service.find_all_categories()
        for category in categories:
            self.pic_categories[category['ABBREVIATION']] = category['CATEGORY']
            self.category_id_abbrevs[category['ABBREVIATION']] = category['ID']

    def determine_category(self, category):
        logger = self.log_utils.get_log(self.name, "")

        first_catgry = category[0:1]
        existed = self.pic_categories.has_key(first_catgry)
        if existed is False:
            logger.info("WARN - No appropriate category [%s] found", category)
            return

        return self.pic_categories.get(first_catgry)

    #: check if the image exists
    def is_img_exist(self, img_name = None, domain_id = None, category_id = None):
        return self.image_persistent_service.is_img_exists(img_name, domain_id, category_id)

    def determine_relative_path(self, domain_id = None, category = None):
        domain = self.domain_persistent_service.find_domain_by_id(domain_id)
        if domain is None:
            raise RuntimeError("No domain found according to ID [%]", domain_id)

        domain_abbr = domain['ABBREVIATION']
        category_sub_folder = self.determine_category(category)

        if domain_abbr is None:
            raise RuntimeError("No domain abbreviation specified")
        if category_sub_folder is None:
            raise RuntimeError("No category specified")

        return domain_abbr + "/" + category_sub_folder

    #: create the directory if absent, and return the path.
    def create_dir_if_absent(self, relative_path = None):
        the_path_to_store_img = self.path_to_save_img + "/" + relative_path
        if os.path.exists(the_path_to_store_img) is False:
            os.makedirs(the_path_to_store_img)

        return the_path_to_store_img

    #: the full file name, without path info
    def determine_file_name(self, img_url = None, category = None):
        if img_url is None:
            raise RuntimeError("Image url address MUST be specified")

        last_forward_slash_idx = img_url.rfind("/")
        question_idx = img_url.rfind("?")

        if question_idx < 0:
            full_file_name = img_url[last_forward_slash_idx + 1: ]
        else:
            full_file_name = img_url[last_forward_slash_idx + 1: question_idx]

        return category + full_file_name

    #: get the file name without suffix, which identifies the file type
    def get_file_name_without_suffix(self, full_file_name = None):
        if full_file_name is None:
            return None

        dot_idx = full_file_name.rfind(".")
        if dot_idx >= 0:
            file_name_without_suffix = full_file_name[0: dot_idx]
        else:
            file_name_without_suffix = full_file_name

        return file_name_without_suffix

    def download_and_save(self, img_url, category, domain_id = None, parent_img_id = None):
        logger = self.log_utils.get_log(self.name, "")
        logger.debug("DEBUG - download and save img_url = %s, category = %s, domain_id = %s, parent_img_id = %s", img_url, category, domain_id, parent_img_id)

        full_file_name = self.determine_file_name(img_url, category)
        file_name_without_suffix = self.get_file_name_without_suffix(full_file_name)
        category_id = self.category_id_abbrevs.get(category)

        #: check if file already exists in local
        #: if exists, then do not download anymore
        if parent_img_id is None:
            if self.is_img_exist(file_name_without_suffix, domain_id, category_id) is True:
                logger.debug("DEBUG - Found that file [%s] already exists to url address [%s]", file_name_without_suffix, img_url)
                return None

        relative_store_path = self.determine_relative_path(domain_id, category)
        path_to_store_img = self.create_dir_if_absent(relative_path=relative_store_path)
        dest_file = path_to_store_img + "/" + full_file_name
        urlopener = urllib.URLopener()
        # download the image stream
        fp = urlopener.open(img_url)
        data = fp.read()
        # write it as byte
        dest = open(dest_file, "w+b")
        dest.write(data)
        dest.close()

        #: after save it to local file system, persistent the data to underlying database
        if parent_img_id is None:
            last_img_id = self.image_persistent_service.insert_and_get_id(file_name_without_suffix, full_file_name, relative_store_path, category_id, domain_id)
            logger.debug("----------------------->>Returned last image id = %s", last_img_id)
            return last_img_id

        return self.image_detail_persistent_service.insert_and_get_id(file_name_without_suffix, full_file_name, relative_store_path, parent_img_id)
