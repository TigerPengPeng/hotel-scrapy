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

def parse_hotel_id(jpg_url):
    return jpg_url.split("/")[-2]

# get property from settings file
# 只支持key=value的格式
def get_property_from_settings(property_name):
    settings_file = get_file_path() + "/settings.py"
    file_content = read_file(settings_file)
    image_path_index = file_content.find(property_name)
    if image_path_index == -1:
        raise Exception(property_name + "配置为空, 请配置")
    else:
        if file_content[image_path_index-1] == "#":
            raise Exception(property_name + "配置被注解, 请删除注解")
	else:
	    begin_index = image_path_index
	    end_index = image_path_index
	    while (file_content[end_index] != "\n"):
	        end_index = end_index + 1
	    return file_content[begin_index:end_index].split("=")[1].strip()
	        
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

