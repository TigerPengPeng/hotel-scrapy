#!/usr/bin/python
# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from singleton import Singleton

class DropSymbol(Singleton):
    def __init__(self, init_drop_str_list):
        self.black_set = set(["▪","●",".","–","(",")"," ","\t","（","）","-","?",",","，","•","·"])
        if init_drop_str_list is not None:
            for drop_str in init_drop_str_list:
                self.black_set.add(drop_str)

    def drop(self, str):
        for sym in self.black_set:
            str = str.replace(sym, "")
        return str

if __name__ == "__main__":
    drop = DropSymbol(["北京"])
    str_y = "北京酒仙桥如家酒店"
    print drop.drop(str_y)


