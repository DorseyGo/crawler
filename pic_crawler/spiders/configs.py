#: ------------------------------------------------
#: FileName:    configs.py
#: Author:  DORSEy Q F TANG
#: Date:    17 Jan 2017
#: Description: a utility class which is used to read configration
#: ------------------------------------------------

import ConfigParser

#: configuration reader to read the configuration from the file specified
#: if there is no conf specified in constructor, then default configuration will be read
class Configs():

    # the config parser
    config = None

    def __init__(self, conf=None):
        if conf is None:
            self.__conf = "configs.conf"
        else:
            self.__conf = conf

    def __readconf__(self):
        if self.config is None:
            self.config = ConfigParser.SafeConfigParser()
            if self.__conf:
                try:
                    self.config.read(self.__conf)
                except IOError, e:
                    raise Exception("Read file exception", self.__conf)
            else:
                raise Exception("Conf not specified")

        return self.config

    #: read configuration in db section
    def dbconf(self, key):
        if key is None:
            raise Exception("key should be specified", key)

        self.config = self.__readconf__()
        return self.config.get('db', key)
