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


# 获取时间的列表。默认从20180101到今天，可修改。
def get_time(start_time="2019-01-01", end_time=str(datetime.datetime.now().date())):
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
    title_num_1, title_num_2 = 0, 0
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

        # data3 港股通(沪)十大成交股
        data3 = re.findall(r'var DATA3 = (.*?);', response)[0]
        data3 = json.loads(data3)

        # 若data3里面已经有了data4的数据,则跳过
        item_dict = set()
        for i in data3.get("data"):
            item = dict()
            # 基本信息
            item["marketType"] = i.get("MarketType")
            item["date_time"] = i.get("DetailDate")
            item["date_time"] = item["date_time"].replace('T00:00:00', '')
            item["rank"] = str(int(i.get("Rank")))
            item["code"] = "\t" + i.get("Code")
            item["name"] = i.get("Name")
            item["close"] = i.get("Close")
            item["changePercent"] = i.get("ChangePercent")
            # 单位亿，净买入，买入，卖出，成交额（买+卖）
            # 港股通（沪）
            item["net_in_h"] = round(i.get("GGTHJME") / 10 ** 8, 2) if i.get("GGTHJME") != "-" else 0
            item["in_h"] = round(i.get("GGTHMRJE") / 10 ** 8, 2) if i.get("GGTHMRJE") != "-" else 0
            item["out_h"] = round(i.get("GGTHMCJE") / 10 ** 8, 2) if i.get("GGTHMCJE") != "-" else 0
            item["total_h"] = round(i.get("GGTHCJJE") / 10 ** 8, 2) if i.get("GGTHCJJE") != "-" else 0
            # 港股通（深）
            item["net_in_s"] = round(i.get("GGTSJME") / 10 ** 8, 2) if i.get("GGTSJME") != "-" else 0
            item["in_s"] = round(i.get("GGTSMRJE") / 10 ** 8, 2) if i.get("GGTSMRJE") != "-" else 0
            item["out_s"] = round(i.get("GGTSMCJE") / 10 ** 8, 2) if i.get("GGTSMCJE") != "-" else 0
            item["total_s"] = round(i.get("GGTSCJJE") / 10 ** 8, 2) if i.get("GGTSCJJE") != "-" else 0
            # 港股通合计（沪+深）
            item["net_in"] = round(i.get("GGTJME") / 10 ** 8, 2) if i.get("GGTJME") != "-" else 0
            item["total"] = round(i.get("GGTCJL") / 10 ** 8, 2) if i.get("GGTCJL") != "-" else 0
            print("data3", item), save_item_in_csv(item, "nanxiang_20stock_{}.csv".format(str_now_day),
                                                   self.title_num_2)
            self.title_num_2 = 1
            item_dict.add(item.get("code"))

        # data4 港股通(深)十大成交股
        data4 = re.findall(r'var DATA4 = (.*?);', response)[0]
        data4 = json.loads(data4)
        for i in data4.get("data"):
            item = dict()
            # 若data3里面已经有了data4的数据,则跳过
            if "\t" + i.get("Code") in item_dict:
                continue
            # 基本信息
            item["marketType"] = i.get("MarketType")
            item["date_time"] = i.get("DetailDate")
            item["date_time"] = item["date_time"].replace('T00:00:00', '')
            item["rank"] = str(int(i.get("Rank"))) if i.get("Rank") != "-" else 0
            item["code"] = "\t" + i.get("Code")
            item["name"] = i.get("Name")
            item["close"] = i.get("Close")
            item["changePercent"] = i.get("ChangePercent")
            # 单位亿，净买入，买入，卖出，成交额（买+卖）
            # 港股通（沪）
            item["net_in_h"] = round(i.get("GGTHJME") / 10 ** 8, 2) if i.get("GGTHJME") != "-" else 0
            item["in_h"] = round(i.get("GGTHMRJE") / 10 ** 8, 2) if i.get("GGTHMRJE") != "-" else 0
            item["out_h"] = round(i.get("GGTHMCJE") / 10 ** 8, 2) if i.get("GGTHMCJE") != "-" else 0
            item["total_h"] = round(i.get("GGTHCJJE") / 10 ** 8, 2) if i.get("GGTHCJJE") != "-" else 0
            # 港股通（深）
            item["net_in_s"] = round(i.get("GGTSJME") / 10 ** 8, 2) if i.get("GGTSJME") != "-" else 0
            item["in_s"] = round(i.get("GGTSMRJE") / 10 ** 8, 2) if i.get("GGTSMRJE") != "-" else 0
            item["out_s"] = round(i.get("GGTSMCJE") / 10 ** 8, 2) if i.get("GGTSMCJE") != "-" else 0
            item["total_s"] = round(i.get("GGTSCJJE") / 10 ** 8, 2) if i.get("GGTSCJJE") != "-" else 0
            # 港股通合计（沪+深）
            item["net_in"] = round(i.get("GGTJME") / 10 ** 8, 2) if i.get("GGTJME") != "-" else 0
            item["total"] = round(i.get("GGTCJL") / 10 ** 8, 2) if i.get("GGTCJL") != "-" else 0
            print("data4", item), save_item_in_csv(item, "nanxiang_20stock_{}.csv".format(str_now_day),
                                                   self.title_num_2)
            self.title_num_2 = 1
