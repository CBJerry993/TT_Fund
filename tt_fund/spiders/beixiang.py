# -*- coding: utf-8 -*-
import scrapy
import json
import re
import requests
from tt_fund.settings import str_now_day
from tt_fund.settings import save_item_in_csv

"""
笔者有代码洁癖，有更清晰简单的coding方法可以联系我
微信cbj1946599315，特此说明！
-----------------------------------
启动方式：scrapy crawl spider.name
文件名：beixiang.py
本程序获取北向资金每日流向 http://data.eastmoney.com/hsgt/index.html  
上海 MarketType=1, 深圳MarketType=3（对应深圳成指）
-----------------------------------
"""


class BeixiangSpider(scrapy.Spider):
    name = 'beixiang'
    allowed_domains = ['eastmoney.com']
    # 表头仅存一次
    title_num = 0
    # 获取页码数
    total_page_list = []
    for markeyType in ["1", "3"]:
        response = requests.get(
            'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?'
            'type=HSGTHIS&token=70f12f2f4f091e459a279469fe49eca5&filter=(MarketType=' + markeyType +
            ')&js=var%20ZnhKMpur={%22data%22:(x),%22pages%22:(tp)}&ps=20&p=3&sr=-1&st=DetailDate&rt=52598322')
        response = re.findall(r'=(.*?)$', response.text)[0]
        response = json.loads(response)
        total_page_list.append(response.get("pages"))
    total_page_sh, total_page_sz = total_page_list[0], total_page_list[1]

    start_urls = []
    for i in range(1, total_page_sh + 1):
        url = 'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGTHIS&' \
              'token=70f12f2f4f091e459a279469fe49eca5&filter=(MarketType=1)&js=var SbHCvwIt=' \
              '{"data":(x),"pages":(tp)}&ps=20&p=%s&sr=-1&st=DetailDate&rt=52541396' % i
        start_urls.append(url)

    for j in range(1, total_page_sz + 1):
        url = 'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGTHIS&' \
              'token=70f12f2f4f091e459a279469fe49eca5&filter=(MarketType=3)&js=var SbHCvwIt=' \
              '{"data":(x),"pages":(tp)}&ps=20&p=%s&sr=-1&st=DetailDate&rt=52541396' % j
        start_urls.append(url)

    # 1.北向资金每日流向
    def parse(self, response):
        response = response.text
        response = re.findall(r'=(.*?)$', response)[0]
        response = json.loads(response)
        for i in response.get("data"):
            item = dict()
            item["marketType"] = i.get("MarketType")
            item["datetime"] = i.get("DetailDate")
            item["datetime"] = item["datetime"].replace('T00:00:00', '')
            item["total_net_in"] = round(i.get("DRCJJME") / 100, 2)  # 当日成交净买额
            item["total_in"] = round(i.get("MRCJE") / 100, 2)  # 买入成交额
            item["total_out"] = round(i.get("MCCJE") / 100, 2)  # 卖出成交额
            item["today_in"] = round(i.get("DRZJLR") / 100, 2)  # 当日资金流入 同花顺是这个！包含了当日成交净买额 + 申报未成交的部分
            item["grand_total_in"] = round(i.get("LSZJLR") / 100, 2)  # 历史资金累计流入 当日资金流入的合计
            item["today_balance"] = round(i.get("DRYE") / 100, 2)  # 当日余额
            item["stock_code"] = i.get("LCGCode")
            item["stock"] = i.get("LCG")
            item["stock_up"] = round(i.get("LCGZDF"), 2)
            item["sz_index"] = i.get("SSEChange")
            item["sz_index_percent"] = round(i.get("SSEChangePrecent") * 100, 2)
            print(item), save_item_in_csv(item, "beixiang_{}.csv".format(str_now_day), self.title_num)
            self.title_num = 1
