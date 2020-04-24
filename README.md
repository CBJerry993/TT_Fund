tt_fund 使用必读

#### 版本：v1.0.20200424

#### 启动方式：scrapy crawl spider.name

本程序从天天基金网采集数据，目前包含下面5个爬虫。根据实际需要，有选择性的爬取即可。

- 一、北向资金每日流向  
- 二、北向资金每日前20大交易股  
- 三、基金公司情况  
- 四、基金排名每日涨跌情况  
- 五、大盘（上证指数、深圳成指、创业板指）每日涨跌情况 

#### 说明：阅读前可以点击原网址查看爬取的目标样式！

---

## 一、北向资金每日流向

- [原网址](http://data.eastmoney.com/hsgt/index.html)

  ![](https://upload-images.jianshu.io/upload_images/19723859-bc428d99f8ab84b9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

  

- 文件名：beixiang.py （上海MarketType=1, 深圳MarketType=3）

- 字段含义

  爬取基本上按照原网址格式，理解起来简单。根据天天基金网提示，值得注意的有两点。1、当日资金流入`today_in`包含两个部分：已经成交的和已申报未成交的。2、当日净买额`today_net_in` = 买入`total_in`-卖出`total_out` 。 一般分析使用的是净买额为当日资金流入`today_in`。

  | 爬取的字段名称   | 含义                                                         |
  | ---------------- | ------------------------------------------------------------ |
  | marketType       | 市场类型：1代表上海，3代表深圳                               |
  | datetime         | 时间                                                         |
  | total_net_in     | 当日成交净买额                                               |
  | total_in         | 买入额                                                       |
  | total_out        | 卖出额                                                       |
  | today_in         | 当日资金流入                                                 |
  | grand_total_in   | 历史累计流入                                                 |
  | today_balance    | 当日余额                                                     |
  | stock_code       | 领涨股代码                                                   |
  | stock            | 领涨股名称                                                   |
  | stock_up         | 领涨股涨跌幅                                                 |
  | sz_index         | 指数（上证或者深圳成指数，根据marketType来确定。1代表上海，3代表深圳） |
  | sz_index_percent | 指数涨跌幅                                                   |

  

## 二、北向资金每日前20大交易股

- [原网址](http://data.eastmoney.com/hsgt/top10/2020-01-02.html)，分沪股通10大交易股和深股通10大交易股。

- 文件名：beixiang_20stock.py

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
