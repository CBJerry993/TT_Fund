# -*- coding: utf-8 -*-
import scrapy
import json
import re
from tt_fund.settings import str_now_day
from tt_fund.settings import save_item_in_csv

"""
各爬虫说明详见github项目 https://github.com/CBJerry993/tt_fund
"""


class IndexSpider(scrapy.Spider):
    name = 'market_index'
    allowed_domains = ['eastmoney.com/']
    # 表头仅存一次
    title_num_1 = 0
    # 上证指数、深圳成指、创业板指
    cid_list = ["1.000001", "0.399001", "0.399006"]
    # format设置查询的开始和结束日期
    start_urls = ['http://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery1124016963078166077672_1576074523699&'
                  'secid={}&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58&'
                  'klt=101&fqt=0&beg={}&end={}'.format(cid, "19900101", "20300101") for cid in cid_list]

    # 上证指数、深圳成指、创业板指每日涨跌幅
    def parse(self, response):
        response = re.findall(r'\((.*?)\);$', response.text)[0]
        response = json.loads(response)
        print(response)
        for i in response.get("data").get("klines"):
            item = {"code": response.get("data").get("code"), "name": response.get("data").get("name"),
                    "datetime": i.split(",")[0], "price_start": i.split(",")[1], "price_end": i.split(",")[2],
                    "price_max": i.split(",")[3], "price_min": i.split(",")[4], "amount": i.split(",")[5],
                    "value": i.split(",")[6], "swing": i.split(",")[7]}
            print(item), save_item_in_csv(item, "market_index_{}.csv".format(str_now_day), self.title_num_1)
            self.title_num_1 = 1
