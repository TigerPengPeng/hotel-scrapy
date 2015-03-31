#!/bin/bash
# Program:
#      Function: This Program will send email 
# History:
# 2015/01/17      Peng.Huang          First release

scrapy_type=$1
log_file=$2
result=$3
echo "====================发送邮件参数===================="
echo scrapy_type: ${scrapy_type} 
echo log_file: ${log_file}
echo result: ${result}
console_log=logs/console/${log_file}
echo console_log: ${console_log} 
echo "====================发送邮件参数===================="

nohup scrapy crawl email -a scrapy_type=${scrapy_type} -a log_file=${log_file} -a result=${result} >> ${console_log} 2>&1 & 
