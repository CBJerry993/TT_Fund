# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from tt_fund.settings import str_now_day
from tt_fund.settings import save_item_in_csv


class ManagerSpider(scrapy.Spider):
    name = 'manager'
    allowed_domains = ['eastmoney.com']
    total_page = 53  # 根据此url修改总页数 http://fund.eastmoney.com/manager/
    start_urls = ["http://fund.eastmoney.com/Data/FundDataPortfolio_Interface.aspx?" \
                  "dt=14&mc=returnjson&ft=all&pn=50&pi={}&sc=abbname&st=asc".format(i) for i in range(total_page)]

    title_num = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
            )

    # 基金经理列表页
    def parse(self, response):
        response = response.text
        response = response.replace('var returnjson= ', '')
        response = response.replace('record', '"record"')
        response = response.replace('pages', '"pages"')
        response = response.replace('curpage', '"curpage"')
        response = response.replace('data', '"data"')
        response = eval(response)  # dict
        for i in response.get("data"):
            item = dict()
            item["manager_id"] = i[0]
            item["manager_name"] = i[1]
            item["company_id"] = i[2]
            item["company_name"] = i[3]
            yield scrapy.Request(
                "http://fund.eastmoney.com/manager/{}.html".format(item.get("manager_id")),
                callback=self.parse_manager_detail,
                meta={"item": item},
            )

    # 基金经理详情
    def parse_manager_detail(self, response):
        item = response.meta.get("item")
        manager_id, manager_name, company_id, company_name = item.get("manager_id"), item.get("manager_name"), item.get(
            "company_id"), item.get("company_name")
        response = etree.HTML(response.text)
        fund_list = response.xpath("//div[@class='content_in']//tbody/tr")
        for fund in fund_list:
            item = dict()
            item["manager_id"] = manager_id
            item["manager_name"] = manager_name
            item["company_id"] = company_id
            item["company_name"] = company_name
            item["avatar"] = response.xpath("//img[@id='photo']/@src")[0]
            item["start_day"] = response.xpath("//div[@class='right jd ']/text()")[3].strip()
            item["scale"] = response.xpath("//div[@class='gmleft gmlefts ']//span[@class='redText']/text()")[0]
            item["scale"] = eval(item["scale"])
            item["best_reward"] = response.xpath("//div[@class='gmleft']//span[@class='numtext']/span/text()")[0]
            item["description"] = response.xpath("//div[@class='jlinfo clearfix']/div[@class='right ms']/p//text()")[
                -1].strip()
            item["fund_id"] = "\t" + fund.xpath("./td[1]/a/text()")[0]
            item["fund_name"] = fund.xpath("./td[2]/a/text()")[0]
            save_item_in_csv(item, "manager_{}.csv".format(str_now_day), self.title_num)
            self.title_num = 1
            print(item)
