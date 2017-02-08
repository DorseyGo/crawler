#: ------------------------------------------------
#: FileName:    db_utils.py
#: Author:  DORSEy Q F TANG
#: Date:    15 Jan 2017
#: Description: a utility class which is used to persist desired data
#: into the underlying database.
#: ------------------------------------------------

import MySQLdb
from DBUtils.PooledDB import PooledDB
from configs import Configs
from log_utils import LogUtils
from datetime import datetime

#: used to persistent data to underlying database
class DBManager():

    #: instance for configuration read
    configs = None

    #: instance for the PooledDB
    __pool = None

    #: log file for recording SQL statement execution
    db_log = "db.log"

    name = "dbmanager"

    logutils = LogUtils()

    def __init__(self):
        if self.__pool is None:
            configs = Configs()
            connArgs = {
                'host' : configs.dbconf('db_host'),
                'user' : configs.dbconf('db_user'),
                'passwd': configs.dbconf('db_password'),
                'port': int(configs.dbconf('db_port')),
                'db': configs.dbconf('db_name'),
                'charset': configs.dbconf('db_charset')
            }

            mincached = int(configs.dbconf('db_min_cached'))
            maxcached = int(configs.dbconf('db_max_cached'))
            maxshared = int(configs.dbconf('db_max_shared'))
            maxusage = int(configs.dbconf('db_max_usage'))

            self.__pool = PooledDB(MySQLdb, mincached=mincached, maxcached=maxcached, maxshared=maxshared, maxusage=maxusage, **connArgs)

    def getconn(self):
        return self.__pool.connection()

    def getlog(self):
        return self.logutils.get_log(self.name)

    #: release the connection
    def _release__(self, conn, cursor):
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()

    def insertandgetid(self, sql, params=None):
        conn = self.getconn()
        cursor = conn.cursor()

        try:
            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)

            #rowid = cursor.lastrowid();
            conn.commit()
            #return rowid
        except Exception, e:
            self.getlog().error("ERROR - Failed to execute sql [%s], with parameters [%s]", sql, params)
            print "error", Exception, e
            conn.rollback()
            #: return None to indicate that its failed
            return None
        finally:
            self._release__(conn, cursor)

    def queryone(self, sql, params=None):
        conn = self.getconn()
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)

        try:
            rowcount = 0
            if params is None:
                rowcount = cursor.execute(sql)
            else:
                rowcount = cursor.execute(sql, params)

            if 1 >= rowcount > 0:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()[0]

            return result
        except:
            self.getlog().error("ERROR - Failed to retrieve one record by executing sql [%s], with parameters [%s]", sql, params)
            return None
        finally:
            self._release__(conn, cursor)

    def queryall(self, sql, params=None):
        conn = self.getconn()
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)

        try:
            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)

            return cursor.fetchall()
        except:
            self.getlog().error("ERROR - Failed to query multiple records by executing sql [%s], with parameters [%s]", sql, params)
            return None
        finally:
            self._release__(conn, cursor)

    def update(self, sql, params=None):
        conn = self.getconn()
        cursor = conn.cursor()

        try:
            if params is None:
                rowaffected = cursor.execute(sql)
            else:
                rowaffected = cursor.execute(sql, params)

            conn.commit()
            if rowaffected > 0:
                return True
            else:
                return False
        except:
            self.getlog().error("ERROR - Failed to update by executing sql [%s], with parameters [%s]", sql, params)
            conn.rollback()
            return False
        finally:
            self._release__(conn, cursor)

    def delete(self, sql, params=None):
        conn = self.getconn()
        cursor = conn.cursor()

        try:
            if params is None:
                rowaffected = cursor.execute(sql)
            else:
                rowaffected = cursor.execute(sql, params)

            conn.commit()
            return (True if rowaffected > 0 else False)
        except:
            self.getlog().error("ERROR - Failed to delete by executing sql [%s], with parameters [%s]", sql, params)
            conn.rollback()
            return False
        finally:
            self._release__(conn, cursor)

if __name__ == '__main__':
    dbutils = DBManager()
    result = dbutils.queryone("select * from categories")
    print result['CATEGORY']

    manys = dbutils.queryall("select * from categories")
    for item in manys:
        print item['CATEGORY']

    #sql = "SELECT RULE_4_NAVI_IMG FROM PIC_DOMAINS pd LEFT JOIN PIC_CATEGORIES_2_URL pc2u ON pd.ID = pc2u.DOMAIN_ID AND pc2u.URL_ADDR = %s" %
    params = ("http://www.roer.co.kr/shop/shopbrand.html?xcode=003&type=X", )
    rules = dbutils.queryone("select RULE_4_NAVI_IMG from pic_domains pd left JOIN pic_categories_2_url pc2u ON pd.id = pc2u.domain_id AND pc2u.url_addr = %s", params)
    # rules = dbutils.queryone("select RULE_4_NAVI_IMG from pic_domains pd left JOIN pic_categories_2_url pc2u ON pd.id = pc2u.domain_id AND pc2u.url_addr = 'http://www.roer.co.kr/shop/shopbrand.html?xcode=003&type=X'")
    print str(rules)

    #params = ("hello", "world", "world", 1)
    #id = dbutils.insertandgetid("insert into images(NAME, FULL_NAME, STORE_PATH, CATEGORY_ID) VALUES(%s, %s, %s, %s)", params)
    #print id