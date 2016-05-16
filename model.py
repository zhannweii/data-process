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

    """ 用户信息 start"""

    def getUser(self, intId):
        # 查询用户信息，工作经历，教育经历

        sql = "select id, uid, name, company_id, company_name, position, avatar, gender, rank, loc, trade, trade_category, create_time from user where id = '%s' " % (intId)
        self.db.query(sql)
        userInfo = self.db.fetchOneRow()

        user = {
            'id': userInfo[0],
            'uid': userInfo[1],
            'name': userInfo[2],
            'company_id': userInfo[3],
            'company_name': userInfo[4],
            'position': userInfo[5],
            'avatar': userInfo[6],
            'gender': userInfo[7],
            'rank': userInfo[8],
            'loc': userInfo[9],
            'trade': userInfo[10],
            'trade_category': userInfo[11],
            'create_time': str(userInfo[12]),
        }

        # 添加大头像地址
        user['avatar_big'] = user['avatar'].replace('a160', 'a480');

        
        uid = user['uid']

        # 工作经历
        sql = "select id, uid, name, company_id, company_name, position, description, start_date, end_date, update_time, create_time from work where uid = '%s'" % (uid)
        self.db.query(sql)
        works = [dict(id=row[0], uid=row[1], name=row[2], company_id=row[3], company_name=row[4], position=row[5], description=markdown.markdown(row[6], extensions=['markdown.extensions.nl2br']), start_date=row[7], end_date=row[8], update_time=str(row[9]), create_time=str(row[10])) \
                 for row in self.db.fetchAllRows()]

        # 教育经历 
        sql = "select id, uid, name, school, department, degree, start_date, end_date, update_time, create_time from education where uid = '%s'" % (uid)
        self.db.query(sql)
        edus = [dict(id=row[0], uid=row[1], name=row[2], school=row[3], department=row[4], degree=row[5], start_date=row[6], end_date=row[7], update_time=str(row[8]), create_time=str(row[9])) \
                 for row in self.db.fetchAllRows()]

        return {
            'user': user,
            'works': works,
            'edus': edus,
        }

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
