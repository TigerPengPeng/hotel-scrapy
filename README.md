basic spider demos to scrapy Ctrip web station
========================================================

@author:            peng.huang
@email:             huangpengssdut@126.com
@date:              2015-05-08
@update content: 补充上次提交未更新的README文件以及重构KDTree
1. 用Shingling算法和LCS算法判断字符串相似度之前，先去除字符串中的特殊字符和城市名称
2. 重构KDTree


@author:            peng.huang
@email:             huangpengssdut@126.com
@date:              2015-05-01
@update content: 补充添加LCS算法对酒店名称判重
1. 完成LCS算法部分
2. 在导入酒店数据的过程中，添加LCS算法筛选出新增酒店


@author:            peng.huang
@email:             huangpengssdut@126.com
@date:              2015-04-02
@update content: 将抓取的ctrip的酒店数据导入到local数据库
1. 导入过程中涉及酒店名称判重，使用kdtree, shingling算法来去除重复酒店
2. 使用shingling算法还不足以筛选出重复的酒店，下次提交需添加算法来筛选重复酒店



@author:            peng.huang
@email:             huangpengssdut@126.com
@date:              2015-04-02
@update content:    detailed README.md

This is a spider project.
Use Django to manager model.
Use Scrapy to scrapy web station.

It scrapys hotel informations, hotel images, hotel reviews,
and record logs, also, send email when scrapy completed.


Thanks and best wishes
