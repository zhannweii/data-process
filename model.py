#!/usr/local/bin python3
# -*- coding: utf8 -*-

'''封装Model

日期：2016-05-16
作者：zhannweii
'''

# 标准库

# 第三方库
import ConfigParser
import redis
import markdown

# 应用程序自有库
import mysqlClass



class Model(object):
    """docstring for Model"""
    db = None    # mysql

    def __init__(self):

        if not self.db:
            self.db = self.connectDB()

    """ 连接相关资源 start"""

    def connectDB(self):
        """连接mysql"""
        cf = ConfigParser.ConfigParser()
        cf.read('conf/config.ini')

        dbconfig = {
            'host': cf.get('aliyun_db', 'host'), 
            'port': cf.getint('aliyun_db', 'port'), 
            'user': cf.get('aliyun_db', 'user'), 
            'passwd': cf.get('aliyun_db', 'passwd'), 
            'db': 'taiji'
        }
                db = mysqlClass.mysqlClass(dbconfig)
                return db

    def getInfo(self):
        """ test for use"""
                username = 'zhangwei41'    
        sql = "select * from user_log where username = '%s' " % (username)
        self.db.query(sql)
        # userInfo = self.db.fetchOneRow()
        userInfo = self.db.fetchAllRows()
                return userInfo

    def __del__(self):
        """ 资源释放（GC自动调用）"""
        if self.db is not None:
            self.db.close()

if __name__ == '__main__':
    # main()
    # pass
    instance = Model()
    aa = instance.getInfo()
    for i in aa:
        print i
        print '<br/>'
    print 'aaa'
