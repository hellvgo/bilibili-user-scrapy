# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy import log

from bilibili_user_scrapy import settings
from bilibili_user_scrapy.items import BilibiliUserScrapyItem

class BilibiliUserScrapyPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("""select * from bilibili_user_info where id=%d""", item['uid'])
            ret = self.cursor.fetchone()
            if ret:
                sql = """update bilibili_user_info set id=%d,name=%s,sex=%s,coins=%d,
                regtime=%s,birthday=%s,place=%s,fans=%d,friend=%d,attention=%d,level=%d,
                exp=%d where id=%d"""%(
                    item["uid"],item["name"],item["sex"],
                    item["coins"],item["regtime"],item["birthday"],
                    item["place"],item["fans"],item["friend"],
                    item["attention"],item["level"],item["exp"],item["uid"])
                self.cursor.execute(sql)
            else:
                sql = """insert into bilibili_user_info(
                id,name,sex,coins,regtime,birthday,place,
                fans,friend,attention,level,exp) 
                values(%d,%s,%s,%d,%s,%s,%s,%d,%d,%d,%d,%d)"""%(
                    item["uid"],item["name"],item["sex"],
                    item["coins"],item["regtime"],item["birthday"],
                    item["place"],item["fans"],item["friend"],
                    item["attention"],item["level"],item["exp"])
                self.cursor.execute(sql)
            self.connect.commit()
        except Exception as error:
            print("error")
        return item

    # @classmethod
    # def from_setting(cls, settings):
    #     dbparams=dict(
    #         host=settings['MYSQL_HOST'],#读取settings中的配置
    #         db=settings['MYSQL_DBNAME'],
    #         user=settings['MYSQL_USER'],
    #         passwd=settings['MYSQL_PASSWD'],
    #         charset='utf8',#编码要加上，否则可能出现中文乱码问题
    #         cursorclass=MySQLdb.cursors.DictCursor,
    #         use_unicode=False,
    #     )
    #     dbpool=adbapi.ConnectionPool('MySQLdb',**dbparams)#**表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
    #     return cls(dbpool)#相当于dbpool付给了这个类，self中可以得到
    
    # def __init__(self,dbpool):
    #     self.dbpool=dbpool

    # def process_item(self, item, spider):
    #     query = self.dbpool.runInteraction(self._conditional_insert, item)
    #     query.addErrback(self._handle_error,item,spider)
    #     return item

    # def _conditional_insert(self,tx,item):
    #     #print item['name']
    #     sql="insert into bilibili_user_info(\
    #     id,name,sex,coins,regtime,birthday,place,\
    #     fans,friend,attention,level,exp)\
    #     values(%d,%s,%s,%d,%s,%s,%s,%d,%d,%d,%d,%d)"
    #     params=(item["uid"],item["name"],item["sex"],
    #         item["coins"],item["regtime"],item["birthday"],
    #         item["place"],item["fans"],item["friend"],
    #         item["attention"],item["level"],item["exp"])
    #     tx.execute(sql,params)

    # def _handle_error(self, failue, item, spider):
    #     print(failue)

