# tt_fund 使用必读


#### 说明：阅读前可以点击原网址查看爬取的目标样式！

#### 版本：v1.0.20200101

#### 启动方式：scrapy crawl spider.name

本程序从天天基金网采集数据，目前包含下面5个爬虫。根据实际需要，有选择性的爬取即可。

- 一、北向资金每日流向  
- 二、北向资金每日前10大流入股  
- 三、基金公司情况  
- 四、基金排名每日涨跌情况  
- 五、大盘（上证指数、深圳成指、创业板指）每日涨跌情况 

---

## 一、北向资金每日流向

- [原网址](http://data.eastmoney.com/hsgt/index.html)
- 文件名：beixiang.py （上海MarketType=1, 深圳MarketType=3）

## 二、北向资金每日前10大流入股

- [原网址](http://data.eastmoney.com/hsgt/top10/2020-01-02.html)

- 文件名：beixiang_10stock.py

## 三、基金公司情况

- [原网址](http://fund.eastmoney.com/Company/default.html)
  - [主页基金列表](http://fund.eastmoney.com/Company/default.html)
  - [基金公司基本信息](http://fund.eastmoney.com/Company/80560392.html)
  - [基金公司股票型和混合型规模、数量、经理数量排名](http://fund.eastmoney.com/Company/home/Gmtable?gsId=80560392&fundType=25)
  - [基金公司下的基金清单](http://fund.eastmoney.com/Company/home/KFSFundNet?gsid=80560392&fundType=25)
  - [公司的10大持仓股票](http://fund.eastmoney.com/Company/f10/gscc_80560392.html)
  - [公司下的行业配置](http://fund.eastmoney.com/Company/f10/hypz_80560392.html)

- 文件名：fund_company.py
  
  



## 四、基金排名每日涨跌情况

- [原网址](http://fund.eastmoney.com/data/fundranking.html)
  - 基金每日收益情况
  - 基金成立以来每日净值
  - 基金基本信息
  - [基金10大持仓股](http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code=320007&topline=10&year=&month=)

- 文件名：fund_earning.py



## 五、大盘（上证指数、深圳成指、创业板指）每日涨跌情况

- 原网址：[上证指数](http://quote.eastmoney.com/zs000001.html)、[深圳成指](http://quote.eastmoney.com/zs399001.html)、[创业板指](http://quote.eastmoney.com/zs399006.html)

- 文件名：market_index.py
