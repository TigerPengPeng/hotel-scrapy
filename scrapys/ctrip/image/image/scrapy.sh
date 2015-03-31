#!/bin/bash
# Program:
#      Function: This Program starts scrapy programs named ctrip_image to scrapy ctrip hotel images
# History:
# 2015/01/22     Peng.Huang          First release

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

# define variables
scrapy_type=$1
cityid=$2
log_file=$3
info_log=logs/info/${log_file}
console_log=logs/console/${log_file}

echo "====================${scrapy_type}脚本参数===================="
echo scrapy_type: ${scrapy_type}
echo cityid: ${cityid}
echo log_file: ${log_file}
echo info_log: ${info_log}
echo console_log: ${console_log}
echo "====================${scrapy_type}脚本参数===================="


#nohup scrapy crawl ctrip_image -a cityid=${cityid} -a info_log=${info_log} >> ${console_log} 2>&1 &
#scrapy crawl ctrip_image -a cityid=${cityid} -a info_log=${info_log} 

# $1 cityid
# $2 info_log 
# $3 console_log
function ctrip_image()
{
    nohup scrapy crawl ctrip_image -a cityid=$1 -a info_log=$2 >> $3 2>&1
    if [ $? -ne 0 ];then
        return 1
    else
        return 0
    fi
}


# $1 scrapy_type
# $2 log_file
# $3 result
function send_email()
{
    cd /home/ray/PythonProjects/scrapy_project/scrapys/manager/send_email/send_email/ 
    if [ $? -ne 0 ];then
        echo "error, cd /home/ray/PythonProjects/scrapy_project/scrapys/manager/send_email/send_email/ failed" 
        exit $?
    fi
    ./email.sh $1 $2 $3
}


ctrip_image ${cityid} ${info_log} ${console_log}
if [ $? -ne 0 ];then
    send_email ${scrapy_type} ${log_file} fail
else
    send_email ${scrapy_type} ${log_file}
fi
