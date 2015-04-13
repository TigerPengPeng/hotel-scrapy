basic spider demos to scrapy Ctrip web station
========================================================

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
