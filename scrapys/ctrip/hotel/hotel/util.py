#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import os.path

def get_file_path():
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    return file_path + "/"


# 处理酒店sub href的函数
def split_city_href(sub_href):
    i = len(sub_href) - 1
    while (i >= 0):
        s = sub_href[i]
	try:
	    int(s)
        except Exception, e:
	    break;
	i = i - 1
    list = []
    if i > -1 and i < len(sub_href) - 1:
        list.append(sub_href[:i+1])
        list.append(int(sub_href[i+1:]))
    elif i == len(sub_href) - 1:
         list.append(sub_href)
         list.append(-1)
    elif i == -1:
        list.append("")
        list.append(int(sub_href))
    return list



# 解析酒店的联系方式
def parse_contract(contract):
    contract = contract.strip()
    telephone_index = contract.rfind("电话")
    fax_index = contract.rfind("传真")

    contract_dic = {} 
    # compare telephone_index and fax_index
    if (telephone_index == fax_index):
        return contract_dic
    if telephone_index < fax_index:
        if telephone_index == -1:
            contract_dic["fax"] = contract.split("传真")[-1].strip()
	else:
	    contract_dic["fax"] = contract.split("传真")[-1].strip()
	    contract_dic["telephone"] = contract.split("传真")[0].split("电话")[-1].strip()
    else:
        if fax_index == -1:
            contract_dic["telephone"] = contract.split("电话")[-1].strip()
	else:
	    contract_dic["telephone"] = contract.split("电话")[-1].strip()
	    contract_dic["fax"] = contract.split("电话")[0].split("传真")[-1].strip()

    return contract_dic


# list转化为string
def list_to_string(list, split):
    for i in range(0, list.__len__()):
        list[i] = str(list[i].encode("utf-8"))

    return split.join(list)


def parse_hotel_star(hotel_star_text):
    length = len(hotel_star_text)
    i = 0
    while i < length:
        try:
	    int(hotel_star_text[i])
	    break
	except Exception, e:
	    i = i + 1

    if len(hotel_star_text) - 1 > i:
        if hotel_star_text[i+1] == ".":
            return hotel_star_text[i:i+3]
        else:
            return hotel_star_text[i]
    else:
        if i < len(hotel_star_text):
            return hotel_star_text[i]
	else:
	    return 0


def parse_hotel_score(score):
    if len(score) > 0:
       if score.find(".") == -1:
           score = float(score[:1])
       else:
           score = float(score[:3])
    else:
        score = 0.0
    return score

# 写入到文件
def write_scrapy_summary_log(parent, file_name, file_text, write_method):
    output = open(os.path.join(parent, file_name), write_method)
    output.write(file_text)
    output.close()


if __name__ == "__main__":
    test = None
    if test:
        print "test"
    else:
        print "none"
