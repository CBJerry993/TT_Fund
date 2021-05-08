[TOC]

## 零、版本信息

版本：v1.0.20210507

更新：

1、北向沪股通、深股通和港股通的爬虫更改了提取url，重写了beixiang_10stock.py

2、检查了爬虫，并爬取部分数据更新到data_temp文件夹

3、考虑到全部数据过大，data_temp文件夹仅为少量数据，全部数据自行参考后文启动爬虫



版本：v1.0.20200424

首次发布！具体功能参考下文。



启动方式：scrapy crawl spider.name

说明：阅读前可以点击原网址查看爬取的目标样式！成功抓取的数据样式在data_temp文件夹内。

本程序从天天基金网采集数据，目前包含下面5个爬虫，基本上涵盖了整个基金市场情况。可以根据实际需要，有选择性的爬取即可。

- 一、北向资金每日流向  
- 二、北向资金每日前20大交易股  
- 三、基金公司情况  
- 四、基金排名每日涨跌情况  
- 五、大盘（上证指数、深圳成指、创业板指）每日涨跌情况 



---

## 一、北向资金每日流向

- [原网址](http://data.eastmoney.com/hsgt/index.html)

![](https://upload-images.jianshu.io/upload_images/19723859-bc428d99f8ab84b9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



- 文件名：beixiang.py （上海MarketType=1, 深圳MarketType=3）

- 字段含义

  爬取基本上按照原网址格式，理解起来简单。根据天天基金网提示，值得注意的有两点。1、当日资金流入`today_in`包含两个部分：已经成交的和已申报未成交的。2、当日净买额`today_net_in` = 买入`total_in`-卖出`total_out` 。 一般分析使用的是净买额为当日资金流入`today_in`。

  | 字段名           | 含义                                                         |
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

- [原网址](http://data.eastmoney.com/hsgt/top10/2020-01-02.html) 

  分沪股通10大交易股和深股通10大交易股

  ![](https://upload-images.jianshu.io/upload_images/19723859-a0102c849829adc3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

  

- 文件名：beixiang_20stock.py

- 字段含义

  当日净流入=当日流入-当日流出； 当日成交额=当日流入+当日流出

  | 字段名        | 含义                           |
  | ------------- | ------------------------------ |
  | marketType    | 市场类型：1代表上海，3代表深圳 |
  | date_time     | 时间                           |
  | rank          | 排名                           |
  | code          | 股票代码                       |
  | name          | 股票名称                       |
  | close         | 当日收盘价                     |
  | changePercent | 当日涨跌幅                     |
  | net_in        | 当日净流入                     |
  | in            | 当日流入                       |
  | out           | 当日流出                       |
  | total         | 当日成交额                     |

  

## 三、基金公司信息

- [原网址](http://fund.eastmoney.com/Company/default.html)
  
  - [基金公司基本信息](http://fund.eastmoney.com/Company/80163340.html)
  
    ![](https://upload-images.jianshu.io/upload_images/19723859-05db1a9edc3b0c54.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
  
    | 字段名              | 含义         |
    | ------------------- | ------------ |
    | company_code        | 基金公司代码 |
    | company_shortName   | 基金公司     |
    | company_name        | 基金公司全称 |
    | position            | 位置         |
    | general_manager     | 总经理       |
    | website_url         | 官网         |
    | tell                | 客服热线     |
    | manager_total_asset | 管理规模     |
    | fund_amount         | 基金数量     |
    | manager_amount      | 经理人数     |
    | publish_date        | 成立日期     |
    | company_property    | 公司性质     |
  
    
  
  - [基金公司规模](http://fund.eastmoney.com/Company/80163340.html)
  
    ![](https://upload-images.jianshu.io/upload_images/19723859-7445eb87d6228845.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
  
    | 字段名                   | 含义                     |
    | ------------------------ | ------------------------ |
    | company_code             | 基金公司代码             |
    | company_shortName        | 基金公司                 |
    | fund_type                | 基金类型                 |
    | fund_scale               | 基金规模（亿元）         |
    | fund_scale_mean          | 平均每家公司基金规模     |
    | fund_scale_rank          | 同类排名                 |
    | fund_amount              | 基金数量                 |
    | fund_amount_mean         | 平均每家公司基金数量     |
    | fund_amount_rank         | 同类排名                 |
    | fund_manager_amount      | 基金经理数量             |
    | fund_manager_amount_mean | 平均每家公司基金经理数量 |
    | fund_manager_amount_rank | 同类排名                 |
  
    
  
  - [基金公司下的基金清单](http://fund.eastmoney.com/Company/80163340.html)
  
    这里就爬取了清单，净值等信息参考第三点基金信息即可。
  
    ![](https://upload-images.jianshu.io/upload_images/19723859-e78dcfe364ff52e1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
  
    | 字段名            | 含义         |
    | ----------------- | ------------ |
    | company_code      | 基金公司代码 |
    | company_shortName | 基金公司     |
    | fund_name         | 基金名称     |
    | fund_code         | 基金代码     |
  
    
  
  - [公司的10大持仓股票](http://fund.eastmoney.com/Company/f10/gscc_80163340.html)
  
    ![](https://upload-images.jianshu.io/upload_images/19723859-d9dfd48aa476ad28.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
  
    | 字段名                | 含义             |
    | --------------------- | ---------------- |
    | company_code          | 基金公司代码     |
    | company_shortName     | 基金公司         |
    | stock_code            | 股票代码         |
    | stock_name            | 股票名称         |
    | havein_mycomanpy_fund | 配置的基金数     |
    | hold_in_value_percent | 配置的基金占比   |
    | stock_amount          | 配置数量（万股） |
    | stock_value           | 配置市值（万元） |
  
    
  
  - [公司下的行业配置](http://fund.eastmoney.com/Company/f10/hypz_80560392.html)
  
    ![](https://upload-images.jianshu.io/upload_images/19723859-40835e36de7a482b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
  
    | 字段名                | 含义             |
    | --------------------- | ---------------- |
    | company_code          | 基金公司代码     |
    | company_shortName     | 基金公司         |
    | industry_category     | 行业             |
    | havein_mycomanpy_fund | 配置的基金数     |
    | hold_in_value_percent | 配置的基金占比   |
    | stock_value           | 配置金额（万元） |
  
    
  
- 文件名：fund_company.py
  
  



## 四、基金信息

- 原网址
  
  - [基金当日排名情况](http://fund.eastmoney.com/data/fundranking.html)
  
    ![](https://upload-images.jianshu.io/upload_images/19723859-53073631694ac79a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

    | 字段名              | 含义                             |
    | ------------------- | -------------------------------- |
    | fund_type           | 基金类型（gp=股票型, hh=混合型） |
    | code                | 基金代码                         |
    | name                | 基金名称                         |
    | today               | 日期                             |
    | net_value           | 净值                             |
    | accumulative_value  | 累计净值                         |
    | rate_day            | 日涨跌幅                         |
    | rate_recent_week    | 最近一周涨跌幅                   |
    | rate_recent_month   | 最近一月涨跌幅                   |
    | rate_recent_3month  | 最近三月涨跌幅                   |
    | rate_recent_6month  | 最近六月涨跌幅                   |
    | rate_recent_year    | 最近一年涨跌幅                   |
    | rate_recent_2year   | 最近两年涨跌幅                   |
    | rate_recent_3year   | 最近三年涨跌幅                   |
    | rate_from_this_year | 今年来涨跌幅                     |
    | rate_from_begin     | 成立来涨跌幅                     |
    | rate_buy            | 购买费率                         |
    | url                 | 基金链接                         |
  
    
  
  - [基金成立以来每日净值](http://fundf10.eastmoney.com/jjjz_005235.html)
  
    ![](https://upload-images.jianshu.io/upload_images/19723859-a4490e8d3190672e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
  
    | 字段名             | 含义                             |
    | :----------------- | -------------------------------- |
    | fund_type          | 基金类型（gp=股票型, hh=混合型） |
    | code               | 基金代码                         |
    | name               | 基金名称                         |
    | date               | 日期                             |
    | total_day          | 总日期数量（代表基金天数）       |
    | net_value          | 净值                             |
    | accumulative_value | 累计净值                         |
    | rate_day           | 当日涨跌幅                       |
    | buy_status         | 当日购买状态                     |
    | sell_status        | 当日赎回状态                     |
  
    
  
  - [基金概况](http://fundf10.eastmoney.com/jbgk_005235.html)
  
    ![](https://upload-images.jianshu.io/upload_images/19723859-0f41b9c82d6a06f1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
  
    | 字段名               | 含义                             |
    | -------------------- | -------------------------------- |
    | full_name            | 基金全称                         |
    | code                 | 基金代码                         |
    | fund_url             | 基金链接                         |
    | type                 | 基金类型（gp=股票型, hh=混合型） |
    | publish_date         | 发行日期                         |
    | setup_date_and_scale | 成立日期/规模                    |
    | asset_scale          | 资产规模                         |
    | amount_scale         | 份额规模                         |
    | company              | 基金公司                         |
    | company_url          | 基金公司链接                     |
    | bank                 | 基金托管人                       |
    | bank_url             | 基金托管人链接                   |
    | manager              | 基金经理                         |
    | manager_url          | 基金经理链接                     |
    | profit_situation     | 成立来分红                       |
    | management_feerate   | 管理费率                         |
    | trustee_feerate      | 托管费率                         |
    | standard_compared    | 业绩比较基准                     |
    | followed_target      | 跟踪标的                         |
  
    
  
  - [基金10大持仓股](http://fundf10.eastmoney.com/ccmx_005235.html)
  
    这是按照季度发布的，一般在季度末的下个月中旬（4、7、10、1月中旬发布上季度持仓股）。
  
    ![](https://upload-images.jianshu.io/upload_images/19723859-9aa64ce5c8622ddc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
  
    | 字段名           | 含义                             |
    | ---------------- | -------------------------------- |
    | code             | 基金代码                         |
    | name             | 基金名称                         |
    | fund_type        | 基金类型（gp=股票型, hh=混合型） |
    | label            | 标签（XXXX年X季度股票投资明细）  |
    | time             | 时间                             |
    | stock_code       | 股票代码                         |
    | stock_name       | 股票名称                         |
    | stock_proportion | 占净值比例                       |
    | stock_amount     | 持有股数（万股）                 |
    | stock_value      | 持有市值（万元）                 |
  
- 文件名：fund_earning.py



## 五、大盘（上证指数、深圳成指、创业板指）每日涨跌情况

- 原网址：[上证指数](http://quote.eastmoney.com/zs000001.html)、[深圳成指](http://quote.eastmoney.com/zs399001.html)、[创业板指](http://quote.eastmoney.com/zs399006.html)

  ![](https://upload-images.jianshu.io/upload_images/19723859-a869d6d5656e5cf4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

  

- 文件名：market_index.py

- 字段含义

  | 字段名      | 含义               |
  | ----------- | ------------------ |
  | code        | 指数代码           |
  | name        | 指数名称           |
  | datetime    | 时间               |
  | price_start | 开盘价             |
  | price_end   | 收盘价             |
  | price_max   | 最高价             |
  | price_min   | 最低价             |
  | amount      | 成交量             |
  | value       | 成交额（单位：元） |
  | swing       | 振幅               |



