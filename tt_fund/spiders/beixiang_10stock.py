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


# 获取时间的列表。默认从20200101到今天，可修改。
def get_time(start_time="2020-01-01", end_time=str(datetime.datetime.now().date())):
    # 时间序列
    import pandas as pd
    a = pd.date_range(start_time, end_time, freq="B")
    date_list = []
    for i in range(len(a.values)):
        date_list.append(str(a.values[i]))
    date_list = [i.replace("T00:00:00.000000000", '') for i in date_list]
    return date_list


def get_item(i, item):
    item["marketType"] = str(int(i.get("MarketType")))
    item["date_time"] = i.get("DetailDate")
    item["date_time"] = item["date_time"].replace('T00:00:00', '')
    item["rank"] = str(int(i.get("Rank")))
    item["code"] = "\t" + i.get("Code")
    item["name"] = i.get("Name")
    item["close"] = i.get("Close")
    item["changePercent"] = i.get("ChangePercent")
    return item


class Beixiang10stockSpider(scrapy.Spider):
    name = 'beixiang_10stock'
    allowed_domains = ['eastmoney.com']

    # 表头仅存一次
    title_num_1, title_num_2 = 0, 0
    # 通过构造日期获取url
    date_list = get_time()

    # url模板，必须加token
    url_temp = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?" \
               "st=DetailDate,Rank&sr=1&ps=10&p=1&type=HSGTCJB&sty={}&" \
               "token=70f12f2f4f091e459a279469fe49eca5&filter=(MarketType={})(DetailDate=^{}^)"
    start_urls = []

    for i in date_list:
        url_1 = url_temp.format("HGT", "1", i)  # 沪股通十大成交股
        url_3 = url_temp.format("SGT", "3", i)  # 深股通十大成交股
        url_2 = url_temp.format("GGT", "2", i)  # 港股通（沪）十大成交股
        url_4 = url_temp.format("GGT", "4", i)  # 港股通（深）十大成交股
        start_urls.extend([url_1, url_3, url_2, url_4])

    def parse(self, response):
        response_url = response.url

        # 沪股通十大成交股
        if "MarketType=1" in response_url:
            response = eval(response.text)
            for i in response:
                item = dict()
                item = get_item(i, item)
                # 单位亿，净买入，买入，卖出，成交额（买+卖）
                item["net_in"] = round(i.get("HGTJME") / 10 ** 8, 2)
                item["in"] = round(i.get("HGTMRJE") / 10 ** 8, 2)
                item["out"] = round(i.get("HGTMCJE") / 10 ** 8, 2)
                item["total"] = round(i.get("HGTCJJE") / 10 ** 8, 2)
                print("沪股通十大成交股:", item)
                save_item_in_csv(item, "beixiang_10stock_{}.csv".format(str_now_day), self.title_num_1)
                self.title_num_1 = 1

        # 深股通十大成交股
        elif "MarketType=3" in response_url:
            response = eval(response.text)
            for i in response:
                item = dict()
                item = get_item(i, item)
                # 单位亿，净买入，买入，卖出，成交额（买+卖）
                item["net_in"] = round(i.get("SGTJME") / 10 ** 8, 2)
                item["in"] = round(i.get("SGTMRJE") / 10 ** 8, 2)
                item["out"] = round(i.get("SGTMCJE") / 10 ** 8, 2)
                item["total"] = round(i.get("SGTCJJE") / 10 ** 8, 2)
                print("深股通十大成交股:", item)
                save_item_in_csv(item, "beixiang_10stock_{}.csv".format(str_now_day), self.title_num_1)
                self.title_num_1 = 1

        # 港股通（沪）十大成交股
        elif "MarketType=2" in response_url:
            response = eval(response.text)
            for i in response:
                item = dict()
                item = get_item(i, item)
                # 单位亿，净买入，买入，卖出，成交额（买+卖）
                item["net_in"] = round(i.get("GGTHJME") / 10 ** 8, 2)
                item["in"] = round(i.get("GGTHMRJE") / 10 ** 8, 2)
                item["out"] = round(i.get("GGTHMCJE") / 10 ** 8, 2)
                item["total"] = round(i.get("GGTHCJJE") / 10 ** 8, 2)
                print("港股通（沪）十大成交股:", item)
                save_item_in_csv(item, "nanxiang_10stock_{}.csv".format(str_now_day), self.title_num_2)
                self.title_num_2 = 1

        # 港股通（深）十大成交股
        elif "MarketType=4" in response_url:
            response = eval(response.text)
            for i in response:
                item = dict()
                item = get_item(i, item)
                item["rank"] = str(int(i.get("Rank1")))
                # 单位亿，净买入，买入，卖出，成交额（买+卖）
                item["net_in"] = round(i.get("GGTSJME") / 10 ** 8, 2)
                item["in"] = round(i.get("GGTSMRJE") / 10 ** 8, 2)
                item["out"] = round(i.get("GGTSMCJE") / 10 ** 8, 2)
                item["total"] = round(i.get("GGTSCJJE") / 10 ** 8, 2)
                print("港股通（深）十大成交股:", item)
                save_item_in_csv(item, "nanxiang_10stock_{}.csv".format(str_now_day), self.title_num_2)
                self.title_num_2 = 1
