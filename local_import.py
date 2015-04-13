#!/usr/bin/env python
# encoding: utf-8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrapy_project.settings")

from app.ctrip.models import Hotel
from app.elong.models import HotelLocal
from common.kdtree import KDTree
from common.shingling import shingStr


class LocalImport:
    # constructor of LocalImport
    def __init__(self):
        hotel_data_list = []
        limit = 1000
        skip = 0
        while (True):
            hotel_local_list = HotelLocal.objects.all()[skip:skip+limit]
            for hotel_local in hotel_local_list:
                hotel_data = self.transfer_tree_node(hotel_local)
                if hotel_data != None:
                    hotel_data_list.append(hotel_data)
            if len(hotel_local_list) < limit:
                break
            skip = skip + limit
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


    # find target_node is duplicate in nearest_node_list
    def shinglingInList(self, target_node, nearest_node_list):
        flag = True
        for each_node in nearest_node_list:
            shinglingValue = shingStr(target_node[2], each_node[2])
            if shinglingValue >= 0.8:
                flag = False
                break
        return flag

    # import hotel list to local database
    def import_data(self, hotel_list):
        for hotel in hotel_list:
            tree_node = self.transfer_tree_node(hotel)
            if tree_node == None:
                continue
            nearest_node_list = self.tree.query(query_point=tree_node, t=10)
            # using shingling algorithms to remove duplicate hotels
            import_flag = self.shinglingInList(tree_node, nearest_node_list)
            # this hotel is not in local database, add it to local database
            if import_flag:
                # transfer it to local object and save it
                local_hotel = HotelLocal.transfer_ctrip_hote_local(hotel)
                local_hotel.save()

    def import_ctrip_data(self):
        skip = 0
        limit = 1000
        while (True):
            hotel_list = Hotel.objects.all()[skip:skip+limit]
            # deal with hotel_list
            self.import_data(hotel_list)
            if len(hotel_list) < limit:
                break
            skip = skip + limit





if __name__ == "__main__":
    ctrip_import = LocalImport()
    #query = ctrip_import.tree.query(query_point=(122, 52, "北京大酒店"), t=10)
    #for item in query:
    #    print item
    ctrip_import.import_ctrip_data()

