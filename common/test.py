#!/usr/bin/env python
# encoding: utf-8
import kdtree


if __name__ == "__main__":
    data = [(1.0,2.0,"北京"),(4.0,0.0,"上海"),(-5.0,2.0,"天津"),(-10.0,5.0,"重庆"),(9.0,8.0,"大连"),(4.0,2.0,"深圳"),(-5.0,2.0,"广州")]
    tree = kdtree.create(point_list=data)
    kdtree.visualize(tree)
    list = tree.search_knn((3.0,4.0,"T"),3)
    for item in list:
        #print (type(item[0]))
        #print (type(item[1]))
        print item[0].data, item[0].axis
        print item[1]
