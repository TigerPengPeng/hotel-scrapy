#coding=utf-8
import sys 
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import os.path

def get_file_path():
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    return file_path + "/" 

# list转化为string
def list_to_string(list, split):
    for i in range(0, list.__len__()):
        list[i] = str(list[i].encode("utf-8"))
    return split.join(list)

# 读取文件
def read_file(absoulte_file_path):
    file_object = open(absoulte_file_path)
    try:
        content = file_object.read()
    finally:
        file_object.close()
    return content

# 写入到文件
def write_scrapy_summary_log(parent, file_name, file_text, write_method):
    output = open(os.path.join(parent, file_name), write_method)
    output.write(file_text)
    output.close()

# 将酒店的href转化为酒店点评页面的href
def parse_review_href(hotel_href):
    href_split = hotel_href.split("/hotel/")
    href_split.insert(1, "hotel/dianping")
    return list_to_string(href_split, "/")


if __name__ == "__main__":
    print parse_review_href("http://hotels.ctrip.com/hotel/87743.html")
