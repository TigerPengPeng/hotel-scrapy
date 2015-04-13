#!/usr/bin/python
# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import ConfigParser

class PropertyLoader:
    def __init__(self, file_path):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(file_path)
        self.map = {}
        for board in self.cf.items("board"):
            self.map[board[0]] = board[1]

    def get_value(self, key):
        return self.map.get(key)


if __name__ == "__main__":
    loader = PropertyLoader("config.properties")
    print loader.map
    print loader.get_value("shingling_value")
    print loader.get_value("nearest_node_number")
    print loader.get_value("database_query_limit")


