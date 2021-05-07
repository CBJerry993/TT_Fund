# -*- coding: utf-8 -*-
import scrapy
import re
from lxml import etree
from tt_fund.settings import str_now_day
from tt_fund.settings import save_item_in_csv

"""
各爬虫说明详见github项目 https://github.com/CBJerry993/tt_fund
"""


class FundCompanySpider(scrapy.Spider):
    name = 'fund_company'
    allowed_domains = ['eastmoney.com']
    start_urls = ['http://fund.eastmoney.com/Company/default.html']
    # 表头仅存一次
    title_num_1, title_num_2_1, title_num_2_2, title_num_2_3, title_num_2_4, title_num_2_5 = [0] * 6
    # 是否需要爬取以下内容
    """
    2.1基金公司基本信息  need_company_info
    2.2基金公司股票型和混合型规模、数量、经理数量排名  need_company_fundscale
    2.3基金公司下的基金清单  need_company_fundlist
    2.4公司的10大持仓股票  need_company_10stock
    2.5公司下的行业配置 need_industry_category
    """
    need_company_info = 1
    need_company_fundscale = 1
    need_company_fundlist = 1
    need_company_10stock = 1
    need_industry_category = 1

    # 1.主页基金列表
    def parse(self, response):
        response = response.body.decode()
        response = etree.HTML(response)
        a_list = response.xpath("//div[@class='sencond-block']/a")
        for a in a_list:
            item = {"company_shortName": a.xpath("./text()")}
            if len(item["company_shortName"]) == 0:
                item["company_shortName"] = None
                continue
            item["company_shortName"] = item["company_shortName"][0]
            item["company_url"] = "http://fund.eastmoney.com" + a.xpath("./@href")[0]
            item["company_code"] = re.findall(r'Company/(.*?)\.html', item["company_url"])[0]
            # print(item)
            # 2.1基金公司基本信息
            if self.need_company_info:
                yield scrapy.Request(
                    "http://fund.eastmoney.com/Company/{}.html".format(item["company_code"]),
                    callback=self.parse_company_info,
                    meta={"item": item},
                )
            # 2.2基金公司股票型和混合型规模、数量、经理数量排名
            if self.need_company_fundscale:
                for fundType in ["25", "27"]:  # funyType=25:股票型 27:混合型
                    yield scrapy.Request(
                        "http://fund.eastmoney.com/Company/home/Gmtable?gsId={}&fundType={}".format(
                            item["company_code"], fundType),
                        callback=self.parse_company_fundscale,
                        meta={"item": item},
                    )
            # 2.3基金公司下的基金清单
            if self.need_company_fundlist:
                for funyType in ["001", "002"]:  # funyType=001是股票型 002是混合型
                    yield scrapy.Request(
                        "http://fund.eastmoney.com/Company/home/KFSFundNet?gsid={}&fundType={}".format(
                            item["company_code"], funyType),
                        callback=self.parse_company_fundList,
                        meta={"item": item},
                    )
            # 2.4公司的10大持仓股票
            if self.need_company_10stock:
                yield scrapy.Request(
                    "http://fund.eastmoney.com/Company/f10/gscc_{}.html".format(item["company_code"]),
                    callback=self.parse_company_10stock,
                    meta={"item": item},
                )
            # 2.5公司下的行业配置
            if self.need_industry_category:
                yield scrapy.Request(
                    "http://fund.eastmoney.com/Company/f10/hypz_{}.html".format(item["company_code"]),
                    callback=self.parse_company_industry_category,
                    meta={"item": item},
                )

    # 2.1基金公司基本信息
    def parse_company_info(self, response):
        item = response.meta.get("item")
        company_code = item.get("company_code")
        company_shortName = item.get("company_shortName")
        response = etree.HTML(response.body.decode())
        item = {"company_code": company_code,
                "company_shortName": company_shortName,
                "company_name": response.xpath("//p[@class='ttjj-panel-main-title']/text()"),
                "position": response.xpath("//div[@class='firm-contact clearfix']/div[1]/p[1]/label/text()"),
                "general_manager": response.xpath("//div[@class='firm-contact clearfix']/div[1]/p[2]/label/text()"),
                "website_url": response.xpath("//div[@class='firm-contact clearfix']/div[2]/p[1]/label/text()"),
                "tell": response.xpath("//div[@class='firm-contact clearfix']/div[2]/p[2]/label/text()"),
                "manager_total_asset": response.xpath("//a[text()='管理规模']/../label/text()"),
                "fund_amount": response.xpath("//div[@class='fund-info']/ul/li[2]/label/a/text()"),
                "manager_amount": response.xpath("//div[@class='fund-info']/ul/li[3]/label/a/text()"),
                "publish_date": response.xpath("//div[@class='fund-info']/ul/li[5]/label/text()"),
                "company_property": response.xpath("//div[@class='fund-info']/ul/li[6]/label/text()")[0].strip()}
        for i_name in ['company_name', 'position', 'general_manager', 'website_url', 'tell',
                       'manager_total_asset', 'fund_amount', 'manager_amount', 'publish_date']:
            item[i_name] = item[i_name][0] if len(item[i_name]) > 0 else None
        print(item), save_item_in_csv(item, "company_info_{}.csv".format(str_now_day), self.title_num_2_1)
        self.title_num_2_1 = 1

    # 2.2基金公司股票型和混合型规模、数量、经理数量排名
    def parse_company_fundscale(self, response):
        item = response.meta.get("item")
        company_code = item.get("company_code")
        company_shortName = item.get("company_shortName")
        response = etree.HTML(response.body.decode())
        item = {"company_code": company_code,
                "company_shortName": company_shortName,
                "fund_type": response.xpath("//tr[1]/th[2]/span/text()"),
                "fund_scale": response.xpath("//tr[2]/td[2]/text()"),
                "fund_scale_mean": response.xpath("//tr[2]/td[3]/text()"),
                "fund_scale_rank": response.xpath("//tr[2]/td[4]/text()"),
                "fund_amount": response.xpath("//tr[3]/td[2]/text()"),
                "fund_amount_mean": response.xpath("//tr[3]/td[3]/text()"),
                "fund_amount_rank": response.xpath("//tr[3]/td[4]/text()"),
                "fund_manager_amount": response.xpath("//tr[4]/td[2]/text()"),
                "fund_manager_amount_mean": response.xpath("//tr[4]/td[3]/text()"),
                "fund_manager_amount_rank": response.xpath("//tr[4]/td[4]/text()")}
        for i_name in ['fund_type', 'fund_scale', 'fund_scale_mean', 'fund_scale_rank', 'fund_amount',
                       'fund_amount_mean', 'fund_amount_rank', 'fund_manager_amount', 'fund_manager_amount_mean',
                       'fund_manager_amount_rank']:
            item[i_name] = item[i_name][0] if len(item[i_name]) > 0 else None
        print(item), save_item_in_csv(item, "company_fundscale_{}.csv".format(str_now_day), self.title_num_2_2)
        self.title_num_2_2 = 1

    # 2.3基金公司下的基金清单
    def parse_company_fundList(self, response):
        item = response.meta.get("item")
        company_code = item.get("company_code")
        company_shortName = item.get("company_shortName")
        response = etree.HTML(response.body.decode())
        tr_list = response.xpath("//tbody/tr")
        for tr in tr_list:
            item = {"company_code": company_code,
                    "company_shortName": company_shortName,
                    "fund_name": tr.xpath("./td/a[1]/text()"),
                    "fund_code": tr.xpath("./td/a[2]/text()")}
            item["fund_name"] = item["fund_name"][0] if len(item["fund_name"]) > 0 else None
            item["fund_code"] = "\t" + tr.xpath("./td/a[2]/text()")[0] if len(item["fund_code"]) > 0 else None
            print(item), save_item_in_csv(item, "company_fund_list_{}.csv".format(str_now_day), self.title_num_2_3)
            self.title_num_2_3 = 1

    # 2.4公司的10大持仓股票
    def parse_company_10stock(self, response):
        item = response.meta.get("item")
        company_code = item.get("company_code")
        company_shortName = item.get("company_shortName")
        response = etree.HTML(response.body.decode())
        tr_list = response.xpath("//table[@class='ttjj-table ttjj-table-hover']/tbody[1]/tr")
        for tr in tr_list:
            item = dict()
            item["company_code"] = company_code
            item["company_shortName"] = company_shortName
            item["stock_code"] = tr.xpath("./td[2]/a/text()")[0]
            item["stock_code"] = "\t" + item["stock_code"]
            item["stock_name"] = tr.xpath("./td[3]/a/text()")[0]
            item["havein_mycomanpy_fund"] = tr.xpath("./td[5]/a/text()")[0]  # 本公司持有基金数
            item["hold_in_value_percent"] = tr.xpath("./td[6]/text()")[0]  # 占总净值比例
            item["stock_amount"] = tr.xpath("./td[7]/text()")[0]  # 持股数(万股)
            item["stock_value"] = tr.xpath("./td[8]/text()")[0]  # 持仓市值(万元)
            print(item), save_item_in_csv(item, "company_10stock_{}.csv".format(str_now_day), self.title_num_2_4)
            self.title_num_2_4 = 1

    # 2.5公司下的行业配置
    def parse_company_industry_category(self, response):
        item = response.meta.get("item")
        company_code = item.get("company_code")
        company_shortName = item.get("company_shortName")
        response = etree.HTML(response.body.decode())
        tr_list = response.xpath("//table[@class='ttjj-table ttjj-table-hover']//tr")[1:]  # [1:]去标题
        for tr in tr_list:
            item = {"company_code": company_code,
                    "company_shortName": company_shortName,
                    "industry_category": tr.xpath("./td[2]/text()")[0],
                    "havein_mycomanpy_fund": tr.xpath("./td[4]/a/text()")[0],
                    "hold_in_value_percent": tr.xpath("./td[5]/text()")[0],
                    "stock_value": tr.xpath("./td[6]/text()")[0]}
            print(item), save_item_in_csv(item, "company_industry_category_{}.csv".format(str_now_day),
                                          self.title_num_2_5)
            self.title_num_2_5 = 1
