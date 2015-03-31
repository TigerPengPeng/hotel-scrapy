#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import os.path

# get scrapy root path
def get_scrapy_root_path():
    scrapy_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir))
    return scrapy_root_path + "/"

# read file and return file content
def read_file(absolute_file_path):
    file_object = open(absolute_file_path)
    try:
        content = file_object.read()
    finally:
        file_object.close()
    return content

# attachs and merage target files from target dirctory
def attachs_and_merge_target_files(root_path, filter_file_name):
    merges = []
    attachs = []
    mimetype = "application/msword"
    for parent, dirs, files in os.walk(root_path):
        for file in files:
            if file == filter_file_name:
                file_full_name = os.path.join(parent, file)
		attachs.append((file_full_name, mimetype, open(file_full_name)))
                merges.append("\n===================================================================================================\n" +
                file_full_name + "\n===================================================================================================\n" +
                read_file(file_full_name))
    return (attachs, "\n\n\n\n\n".join(merges))

if __name__ == "__main__":
    (attachs, merges) = attachs_and_merge_target_files(get_scrapy_root_path() + "ctrip", "2015-02-03.12.log")
    print merges
    print attachs
