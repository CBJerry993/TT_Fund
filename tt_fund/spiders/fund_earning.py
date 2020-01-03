# -*- coding: utf-8 -*-
import scrapy
import re
import json
from lxml import etree
from tt_fund.settings import str_now_day
from tt_fund.settings import save_item_in_csv

"""
版本号：v1.0.20200101
文件名fund_earning.py

笔者有代码洁癖，有更清晰简单的coding方法可以联系我
微信cbj1946599315，特此说明！
-----------------------------------
启动方式：scrapy crawl spider.name
文件名：fund_earning.py
本程序启动后依次获取以下3个部分内容：
1.基金每日收益情况
2.1基金成立以来每日净值（pageSize写2万一次加载完。一个月就写20）
2.2基金基本信息
2.3基金10大持仓股（可以指定年和指定前10大还是20大） http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code=320007&topline=10&year=&month=
-----------------------------------
"""


class FundEarningSpider(scrapy.Spider):
    name = 'fund_earning'
    allowed_domains = ['eastmoney.com']
    # 股票型ft=gp，混合型ft=hh
    start_urls = [
        'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=gp&rs=&gs=0&sc=zzf&st=desc'
        '&qdii=&tabSubtype=,,,,,&pi=1&pn=10000&dx=1&v=0.42187391938911856',
        'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=hh&rs=&gs=0&sc=zzf&st=desc'
        '&qdii=&tabSubtype=,,,,,&pi=1&pn=10000&dx=1&v=0.42187391938911856']
    # 表头仅写入一次
    title_num_1, title_num_2_1, title_num_2_2, title_num_2_3 = 0, 0, 0, 0
    # 是否需要爬取以下内容
    need_fund_earning_perday, need_fund_basic_info, need_fund_position = True, True, True

    # 1.基金每日收益情况
    def parse(self, response):
        fund_type = re.findall(r'kf&ft=(.*?)&rs=&gs=0&sc=zzf&st=desc', response.url)[0]
        response = response.text
        response = re.findall(r"var rankData = (.*?);$", response)[0]
        response = re.findall(r"\[(.*?)]", response)[0]
        fund_list = response.split('"')
        fund_list = [i for i in fund_list if i != ""]
        fund_list = [i for i in fund_list if i != ","]
        for fund in fund_list:
            f = fund.split(",")
            # 为了把0开头的存入，加tab
            item = {"fund_type": fund_type, "code": "\t" + f[0], "name": f[1], "today": f[3], "net_value": f[4],
                    "accumulative_value": f[5], "rate_day": f[6], "rate_recent_week": f[7], "rate_recent_month": f[8],
                    "rate_recent_3month": f[9], "rate_recent_6month": f[10], "rate_recent_year": f[11],
                    "rate_recent_2year": f[12], "rate_recent_3year": f[13], "rate_from_this_year": f[14],
                    "rate_from_begin": f[15], "rate_buy": f[20]}
            item["url"] = "http://fund.eastmoney.com/" + item["code"] + ".html"
            print(item), save_item_in_csv(item, "fund_earning_list_{}.csv".format(str_now_day), self.title_num_1)
            self.title_num_1 = 1

            # 2.1基金成立以来每日净值
            if self.need_fund_earning_perday:
                yield scrapy.Request(
                    "http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery183036648984792081185_1575425405289&"
                    "fundCode={}"
                    "&pageIndex=1&pageSize=20".format(item.get("code").strip()),  # pageSize写2万一次加载完。一个月就写20。
                    headers={"Referer": "http://fundf10.eastmoney.com"},
                    callback=self.parse_fund_earning_perday,
                    meta={"item": item},
                )
            # 2.2基金基本信息
            if self.need_fund_basic_info:
                yield scrapy.Request(
                    "http://fundf10.eastmoney.com/jbgk_{}.html".format(item["code"].strip()),
                    callback=self.parse_fund_basic_info,
                    meta={"item": item},
                )
            # 2.3基金10大持仓股(指定按年)
            if self.need_fund_position:
                yield scrapy.Request(
                    "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={}&topline=10&year=2019"
                    "&month=".format(item["code"].strip()),
                    callback=self.parse_fund_position,
                    meta={"item": item},
                )

    # 2.1基金成立以来每日净值
    def parse_fund_earning_perday(self, response):
        item = response.meta.get("item")
        code = item.get("code")
        fund_type = item.get("fund_type")
        name = item.get("name")
        response = response.text
        data = re.findall(r'\((.*?)\)$', response)[0]
        data = json.loads(data)
        for i in data.get("Data").get("LSJZList"):
            item = {"fund_type": fund_type, "code": code, "name": name, "date": i.get("FSRQ"),
                    "total_day": data.get("TotalCount"), "net_value": i.get("DWJZ"),
                    "accumulative_value": i.get("LJJZ"), "rate_day": i.get("JZZZL"), "buy_status": i.get("SGZT"),
                    "sell_status": i.get("SHZT"), "profit": i.get("FHSP")}
            print(item), save_item_in_csv(item, "fund_earning_perday_{}.csv".format(str_now_day), self.title_num_2_1)
            self.title_num_2_1 = 1

    # 2.2基金基本信息
    def parse_fund_basic_info(self, response):
        item = response.meta.get("item")
        code = item.get("code")
        response = etree.HTML(response.text)
        item = {"full_name": response.xpath("//th[text()='基金全称']/../td[1]/text()"), "code": code,
                "fund_url": 'http://fundf10.eastmoney.com/jbgk_{}.html'.format(code.strip()),
                "type": response.xpath("//th[text()='基金类型']/../td[2]/text()"),
                "publish_date": response.xpath("//th[text()='发行日期']/../td[1]/text()"),
                "setup_date_and_scale": response.xpath("//th[text()='成立日期/规模']/../td[2]/text()"),
                "asset_scale": response.xpath("//th[text()='资产规模']/../td[1]/text()"),
                "amount_scale": response.xpath("//th[text()='份额规模']/../td[2]/a/text()"),
                "company": response.xpath("//th[text()='基金管理人']/../td[1]/a/text()"),
                "company_url": response.xpath("//th[text()='基金管理人']/../td[1]/a/@href"),
                "bank": response.xpath("//th[text()='基金托管人']/../td[2]/a/text()"),
                "bank_url": response.xpath("//th[text()='基金托管人']/../td[2]/a/@href"),
                "manager": response.xpath("//th[text()='基金经理人']/../td[1]//a/text()"),
                "manager_url": response.xpath("//th[text()='基金经理人']/../td[1]//a/@href"),
                "profit_situation": response.xpath("//th[text()='基金经理人']/../td[2]/a/text()"),
                "management_feerate": response.xpath("//th[text()='管理费率']/../td[1]/text()"),
                "trustee_feerate": response.xpath("//th[text()='托管费率']/../td[2]/text()"),
                "standard_compared": response.xpath("//th[text()='业绩比较基准']/../td[1]/text()"),
                "followed_target": response.xpath("//th[text()='跟踪标的']/../td[2]/text()")}
        for i_name in ["full_name", "type", "publish_date", "setup_date_and_scale", "asset_scale", "amount_scale",
                       "company", "company_url", "bank", "bank_url", "manager", "manager_url", "profit_situation",
                       "management_feerate", "trustee_feerate", "standard_compared", "followed_target"]:
            item[i_name] = item[i_name][0] if len(item[i_name]) > 0 else None
        print(item), save_item_in_csv(item, "fund_basic_info_{}.csv".format(str_now_day), self.title_num_2_2)
        self.title_num_2_2 = 1

    # 2.3基金10大持仓股(指定按年)
    def parse_fund_position(self, response):
        item = response.meta.get("item")
        code = item.get("code")
        fund_type = item.get("fund_type")
        name = item.get("name")
        response = response.body.decode()
        response = re.findall(r'var apidata={ content:(.*?),arryear', response)[0]
        response = etree.HTML(response)
        div_list = response.xpath("//div[@class='boxitem w790']")
        for div in div_list:
            label = div.xpath(".//label[@class='left']/text()")[0].strip()
            time_1 = div.xpath(".//label[@class='right lab2 xq505']/font/text()")[0].strip()
            tr_list = div.xpath(".//table[@class='w782 comm tzxq']/tbody/tr")
            for tr in tr_list:
                # 单位万股，万元
                item = {"code": code, "name": name, "fund_type": fund_type, "label": label, "time": time_1,
                        "stock_code": "\t" + tr.xpath("./td[2]/a/text()")[0],  # 为了把0开头的存入，加tab
                        "stock_name": tr.xpath("./td[3]/a/text()"),
                        "stock_proportion": tr.xpath("./td[last()-2]/text()"),  # 持仓占净值比例
                        "stock_amount": tr.xpath("./td[last()-1]/text()"),  # 持仓股数，万股
                        "stock_value": tr.xpath("./td[last()]/text()")}  # 持仓市值，万元
                for i_name in ["stock_name", "stock_proportion", "stock_amount", "stock_value"]:
                    item[i_name] = item[i_name][0] if len(item[i_name]) > 0 else None
                print(item), save_item_in_csv(item, "fund_stock10_{}.csv".format(str_now_day), self.title_num_2_3)
                self.title_num_2_3 = 1
