#!/usr/bin/env python
# encoding: utf-8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrapy_project.settings")

from app.ctrip.models import Hotel
from app.elong.models import HotelLocal
from common.property_loader import ImportConfig
from common.kdtree import KDTree
from common.shingling import shing_str
from common.longest_common_subsequence import longest_common_subsequence_percentage


class LocalImport:
    # constructor of LocalImport
    def __init__(self):
        # load property file
        config = ImportConfig()
        self.shingling_value = config.shingling_value
        self.cls_value = config.cls_value
        self.nearest_node_number = config.nearest_node_number
        self.limit = config.database_query_limit
        print self.shingling_value, self.nearest_node_number, self.limit

        hotel_data_list = []
        skip = 0
        while (True):
            hotel_local_list = HotelLocal.objects.all()[skip:skip+self.limit]
            for hotel_local in hotel_local_list:
                hotel_data = self.transfer_tree_node(hotel_local)
                if hotel_data != None:
                    hotel_data_list.append(hotel_data)
            if len(hotel_local_list) < self.limit:
                break
            skip = skip + self.limit
        self.tree = KDTree.construct_from_data(hotel_data_list)


    # split hotel scott point
    # for example, input:'100.980545043945|22.7850761413574' output:['100.980545043945', '22.7850761413574']
    def split_scott_point(self, scott_point, split):
        return scott_point.split(split)

    # transger hotel model to kdtree node
    def transfer_tree_node(self, hotel_model):
        scott_point = hotel_model.scott_point
        name_ch = hotel_model.name_ch
        scott_point_split = self.split_scott_point(scott_point, "|")
        if len(scott_point_split) == 2 and name_ch != "":
            return (float(scott_point_split[0]), float(scott_point_split[1]), name_ch)
        else:
            return None


    # find target_node is duplicate in nearest_node_list by shingling
    def shingling_in_list(self, target_node, nearest_node_list):
        for each_node in nearest_node_list:
            shinglingValue = shing_str(target_node[2], each_node[2])
            if shinglingValue >= self.shingling_value:
                return False
        return True

    # find target_node is duplicate in nearest_node_list by cls
    def cls_in_list(self, target_node, nearest_node_list):
        for each_node in nearest_node_list:
            cls_value = longest_common_subsequence_percentage(target_node[2], each_node[2])
            if cls_value >= self.cls_value:
                return False
        return True

    # import hotel list to local database
    def import_data(self, hotel_list):
        for hotel in hotel_list:
            tree_node = self.transfer_tree_node(hotel)
            if tree_node == None:
                continue
            nearest_node_list = self.tree.query(query_point=tree_node, t=self.nearest_node_number)
            # using shingling algorithms to remove duplicate hotels
            import_flag = self.shingling_in_list(tree_node, nearest_node_list)
            cls_flag = self.cls_in_list(tree_node, nearest_node_list)
            # this hotel is not in local database, add it to local database
            if import_flag and cls_flag:
                # transfer it to local object and save it
                local_hotel = HotelLocal.transfer_ctrip_hote_local(hotel)
                local_hotel.save()

    def import_ctrip_data(self):
        skip = 0
        while (True):
            hotel_list = Hotel.objects.all()[skip:skip+self.limit]
            # deal with hotel_list
            self.import_data(hotel_list)
            if len(hotel_list) < self.limit:
                break
            skip = skip + self.limit


if __name__ == "__main__":
    #config = ImportConfig()
    #print config.shingling_value, config.nearest_node_number, config.database_query_limit
    ctrip_import = LocalImport()
    ctrip_import.import_ctrip_data()

