#!/usr/bin/python
# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import ConfigParser
from singleton import Singleton

class PropertyLoader:
    def __init__(self, file_path):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(file_path)
        self.map = {}
        for board in self.cf.items("board"):
            self.map[board[0]] = board[1]

    def get_value(self, key):
        return self.map.get(key)


class ImportConfig(Singleton):
    loader = PropertyLoader("config.properties")
    shingling_value = float(loader.get_value("shingling_value"))
    nearest_node_number = int(loader.get_value("nearest_node_number"))
    database_query_limit = int(loader.get_value("database_query_limit"))


if __name__ == "__main__":
    config = ImportConfig()
    print config.shingling_value, config.nearest_node_number, config.database_query_limit
