# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from ganji_crawler.items import *
from ganji_crawler.log import *
from ganji_crawler.helpers import *

from twisted.enterprise import adbapi
import datetime
import MySQLdb.cursors
from ganji_crawler.config import DB_SERVER, DB_CONNECT
import traceback

class GanjiCrawlerPipeline(object):
    insert_sql = """INSERT INTO ws_agents_ganji (%s) VALUES ( %s )"""
    insert_house_sql = """INSERT INTO ws_house_info_14 (%s) VALUES ( %s )"""
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool(DB_SERVER,
            host=DB_CONNECT['host'],
            db=DB_CONNECT['db'],
            user=DB_CONNECT['user'],
            passwd=DB_CONNECT['passwd'],
            port=DB_CONNECT['port'],
            cursorclass=MySQLdb.cursors.DictCursor,
            charset=DB_CONNECT['charset'],
            use_unicode=DB_CONNECT['use_unicode'],
            )
        debug("SQLStorePipeline init")
    def close_spider(self, spider):
        debug("SQLStorePipeline closed")
    def open_spider(self, spider):
        debug("SQLStorePipeline opend")

    def process_item(self, item, spider):
        info("SQLStorePipeline process_item")
        if isinstance(item, JJRItem):
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self._database_error, item)

        if isinstance(item, HouseItem):
            query = self.dbpool.runInteraction(self._conditional_insert_house, item)
            query.addErrback(self._database_error, item)

        return item

    def _conditional_insert(self, tx, item):
        try:
#            tx.execute("SELECT id FROM ws_agents_ganji WHERE info_id = %s", (item['info_id'],))
#            result = tx.fetchone()
#            if result:
#                debug("info already in db: %s" % (item['info_id'],))
#            else:
            # add item record in the db
            debug("Inserting item: %s" % item['url'])
            keys = item.fields.keys()
            fields = u','.join(keys)
            qm = u','.join([u'%s'] * len(keys))
            sql = self.insert_sql % (fields, qm)
            data = [item[k] for k in keys]
            debug(str(sql) + str(data))
            tx.execute(sql, data)

        except Exception, e:
            traceback.print_exc()


    def _conditional_insert_house(self, tx, item):
        try:
#            tx.execute("SELECT id FROM ws_house_info_14 WHERE house_id = %s", (item['house_id'],))
#            result = tx.fetchone()
#            if result:
#                debug("house already in db: %s" % (item['house_id'],))
#            else:
            # add item record in the db
            debug("Inserting item: %s" % item['url'])
            keys = item.fields.keys()
            fields = u','.join(keys)
            qm = u','.join([u'%s'] * len(keys))
            sql = self.insert_house_sql % (fields, qm)
            data = [item[k] for k in keys]
            debug(str(sql) + str(data))
            tx.execute(sql, data)

        except Exception, e:
            traceback.print_exc()


    def _database_error(self, e, item):
        print "Database error: ", e

