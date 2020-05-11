# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import firebirdsql

class BaiduPipeline(object):
    def __init__(self):
        self.conn = firebirdsql.connect(
            host='localhost',
            database='/var/lib/firebird/2.5/data/pazha.fdb',
            port=3050,
            user='SYSDBA',
            password='a5r2t8'
            )
        self.cur = self.conn.cursor()
        
    def process_item(self, item, spider):
        print('='*40)
        print("insert into keyword_contact values(GEN_ID(gen_keyword_contact_id, 1),0,'{}','{}','{}','{}','{}','{}')"
              .format(item['nickname'],item['phone_no'],item['email'],item['languange_code'],item['languange_name'],item['detail']))
        print('='*40)
#         sql="insert into keyword_contact(id,keyword_id,nickname,phone_no,email,languange_code,languange_name,detail) values(GEN_ID(gen_keyword_contact_id, 1),0,s%,s%,s%,s%,s%,s%)"
#         sdata=(item['nickname'],item['phone_no'],item['email'],item['languange_code'],item['languange_name'],item['detail'])
        n=self.cur.execute("insert into keyword_contact values(GEN_ID(gen_keyword_contact_id, 1),0,'{}','{}','{}','{}','{}','{}')"
              .format(item['nickname'],item['phone_no'],item['email'],item['languange_code'],item['languange_name'],item['detail']))
        
        print(n)
        
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()