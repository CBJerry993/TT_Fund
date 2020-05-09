# -*- coding: utf-8 -*-
import scrapy
import json
import re
import datetime
from tt_fund.settings import str_now_day
from tt_fund.settings import save_item_in_csv

"""
各爬虫说明详见github项目 https://github.com/CBJerry993/tt_fund
"""


# 获取时间的列表。默认从20180101到今天，可修改
def get_time(start_time="2018-01-01", end_time=str(datetime.datetime.now().date())):
    # 时间序列
    import pandas as pd
    a = pd.date_range(start_time, end_time, freq="B")
    date_list = []
    for i in range(len(a.values)):
        date_list.append(str(a.values[i]))
    date_list = [i.replace("T00:00:00.000000000", '') for i in date_list]
    return date_list


class Beixiang10Spider(scrapy.Spider):
    name = 'beixiang_20stock'
    allowed_domains = ['eastmoney.com']
    # 表头仅存一次
    title_num_1 = 0
    # 通过构造日期获取url
    date_list = get_time()
    start_urls = []
    for i in date_list:
        start_urls.append("http://data.eastmoney.com/hsgt/top10/{}.html".format(i))

    # 北向资金每一天的十大成交股(沪股通+深股通)
    def parse(self, response):
        response = response.text
        # data1 沪股通十大成交股
        data1 = re.findall(r'var DATA1 = (.*?);', response)[0]
        data1 = json.loads(data1)
        for i in data1.get("data"):
            item = dict()
            item["marketType"] = str(int(i.get("MarketType")))
            item["date_time"] = i.get("DetailDate")
            item["date_time"] = item["date_time"].replace('T00:00:00', '')
            item["rank"] = str(int(i.get("Rank")))
            item["code"] = "\t" + i.get("Code")
            item["name"] = i.get("Name")
            item["close"] = i.get("Close")
            item["changePercent"] = i.get("ChangePercent")
            # 单位亿，净买入，买入，卖出，成交额（买+卖）
            item["net_in"] = round(i.get("HGTJME") / 10 ** 8, 2)
            item["in"] = round(i.get("HGTMRJE") / 10 ** 8, 2)
            item["out"] = round(i.get("HGTMCJE") / 10 ** 8, 2)
            item["total"] = round(i.get("HGTCJJE") / 10 ** 8, 2)
            print(item), save_item_in_csv(item, "beixiang_20stock_{}.csv".format(str_now_day), self.title_num_1)
            self.title_num_1 = 1

        # data2 深股通十大成交股
        data2 = re.findall(r'var DATA2 = (.*?);', response)[0]
        data2 = json.loads(data2)
        for i in data2.get("data"):
            item = dict()
            item["marketType"] = str(int(i.get("MarketType")))
            item["date_time"] = i.get("DetailDate")
            item["date_time"] = item["date_time"].replace('T00:00:00', '')
            item["rank"] = str(int(i.get("Rank")))
            item["code"] = "\t" + i.get("Code")
            item["name"] = i.get("Name")
            item["close"] = i.get("Close")
            item["changePercent"] = i.get("ChangePercent")
            # 单位亿，净买入，买入，卖出，成交额（买+卖）
            item["net_in"] = round(i.get("SGTJME") / 10 ** 8, 2)
            item["in"] = round(i.get("SGTMRJE") / 10 ** 8, 2)
            item["out"] = round(i.get("SGTMCJE") / 10 ** 8, 2)
            item["total"] = round(i.get("SGTCJJE") / 10 ** 8, 2)
            print(item), save_item_in_csv(item, "beixiang_20stock_{}.csv".format(str_now_day), self.title_num_1)
            self.title_num_1 = 1
