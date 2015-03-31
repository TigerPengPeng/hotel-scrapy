#!/bin/bash
# Program:
#      Function: This Program starts Django Server in background and saves server logs into directory ./server-log/
# History:
# 2015/01/13      Peng.Huang          First release
nohup python manage.py runserver 0.0.0.0:80 > server-log/catalina.`date +%Y-%m-%d_%H-%M-%S` 2>&1 &
exit 0
