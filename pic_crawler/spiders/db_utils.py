#: ------------------------------------------------
#: FileName:    db_utils.py
#: Author:  DORSEy Q F TANG
#: Date:    15 Jan 2017
#: Description: a utility class which is used to persist desired data
#: into the underlying database.
#: ------------------------------------------------

import MySQLdb
from DBUtils.PooledDB import PooledDB
import db_configs as DBConfigs

#: used to persistent data to underlying database
class DBManager():


    def __init__(self):
        conn_args = {'host' : DBConfigs['DB_HOST'], 'user' : DBConfigs['DB_USER'], 'passwd' : DBConfigs['DB_PASSWD'],
                     'db': DBConfigs['DB_NAME'], 'charset': DBConfigs['DB_CHARSET']}
        self._pool = PooledDB(MySQLdb, mincached=DBConfigs['DB_MIN_CACHED'], maxcached=DBConfigs['DB_MAX_CACHED'], maxshared=DBConfigs['DB_MAX_SHARED'], maxusage=DBConfigs['DB_MAX_USAGE'], **conn_args)


    def getconn(self):
        return self._pool.connection()


__dbManager = DBManager()


def getconnection():
    return __dbManager.getconn()

def execute_and_getId(sql, param=None):
    conn = getconnection()
    cursor = conn.cursor()
    if param == None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, param)

    id = cursor.lastrowid
    __release__(cursor, conn)


    return id

def queryone(sql):
    conn = getconnection()
    cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    rowcount = cursor.execute(sql)

    if rowcount > 0:
        result = cursor.fetchone()
    else:
        result = None

    __release__(cursor, conn)

    return result

def queryall(sql):
    conn = getconnection()
    cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    rowcount = cursor.execute(sql)

    if rowcount > 0:
        result = cursor.fetchall()
    else:
        result = None

    __release__(cursor, conn)

    return result

def insert_and_getid(sql, param=None):
    conn = getconnection()
    cursor = conn.cursor()

    if param == None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, param)

    id = cursor.lastrowid
    conn.commit()
    __release__(cursor, conn)

    return id

def __release__(cursor, conn):
    cursor.close()
    conn.close()

