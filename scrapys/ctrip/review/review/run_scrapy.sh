#!/bin/bash
# Program:
#      Function: This Program Run Scrapy Shell 
# History:
# 2015/01/22     Peng.Huang          First release

# define variables
scrapy_type=$1
cityid=$2
date=`date +%Y-%m-%d.%H`
log_file=${date}.log
console_log=logs/console/${log_file}

cd /home/ray/PythonProjects/scrapy_project/scrapys/ctrip/review/review/ 
if [ $? -ne 0 ];then
    echo "error, cd /home/ray/PythonProjects/scrapy_project/scrapys/ctrip/review/review/ failed" 
    exit $?
fi

nohup ./scrapy.sh ${scrapy_type} ${cityid} ${log_file} >> ${console_log} 2>&1 &
