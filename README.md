# tt_fund 使用必读


#### 说明：阅读前可以点击原网址查看爬取的目标样式！（原网址在下面每一点有记录）
#### 版本：v1.0.20200101
#### 启动方式：scrapy crawl spider.name
本程序从天天基金网采集数据，目前包含5个爬虫：
- 一、北向资金每日流向  
- 二、北向资金每日前10大流入股  
- 三、基金公司情况  
- 四、基金排名每日涨跌情况  
- 五、大盘（上证指数、创业板指数、深圳成指）涨跌情况 

---

## 一、北向资金每日流向
[原网址](http://data.eastmoney.com/hsgt/index.html)
- 文件名：beixiang.py
- 本程序获取北向资金每日流向 http://data.eastmoney.com/hsgt/index.html  
- 上海 MarketType=1, 深圳MarketType=3（对应深圳成指）

## 二、北向资金每日前10大流入股
原网址：http://data.eastmoney.com/hsgt/top10/2020-01-02.html
- 文件名：beixiang_10stock.py
- 本程序获取北向资金每前10股票 http://data.eastmoney.com/hsgt/top10/2019-12-10.html

## 三、基金公司情况
原网址：http://fund.eastmoney.com/Company/default.html
- 文件名：fund_company.py
本程序获取基金公司信息  
- 1.主页基金列表  http://fund.eastmoney.com/Company/default.html
- 2.1基金公司基本信息  http://fund.eastmoney.com/Company/80560392.html
- 2.2基金公司股票型和混合型规模、数量、经理数量排名  http://fund.eastmoney.com/Company/home/Gmtable?gsId=80560392&fundType=25
- 2.3基金公司下的基金清单  http://fund.eastmoney.com/Company/home/KFSFundNet?gsid=80560392&fundType=25
- 2.4公司的10大持仓股票  http://fund.eastmoney.com/Company/f10/gscc_80560392.html
- 2.5公司下的行业配置  http://fund.eastmoney.com/Company/f10/hypz_80560392.html

## 四、基金排名每日涨跌情况
原网址：http://fund.eastmoney.com/data/fundranking.html
- 文件名：fund_earning.py
本程序启动后依次获取以下3个部分内容：
- 1.基金每日收益情况
- 2.1基金成立以来每日净值（pageSize写2万一次加载完。一个月就写20）
- 2.2基金基本信息
- 2.3基金10大持仓股（可以指定年和指定前10大还是20大） 
http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code=320007&topline=10&year=&month=

## 五、大盘（上证指数、创业板指数、深圳成指）涨跌情况
原网址：http://quote.eastmoney.com/zs000001.html
- 文件名：文件名market_index.py
本程序启动后依次获取以下部分内容：
- 1.上证、深成、创业板指数每日涨跌幅
  - http://quote.eastmoney.com/zs000001.html
  - http://quote.eastmoney.com/zs399001.html
  - http://quote.eastmoney.com/zs399006.html

---



