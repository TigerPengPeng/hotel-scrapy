#!/usr/bin/env python
# encoding: utf-8
import kdtree


if __name__ == "__main__":
    data = [(1.0,2.0,"A"),(4.0,0.0,"B"),(-5.0,2.0,"C"),\
            (-10.0,5.0,"D"),(9.0,8.0,"E"),(4.0,2.0,"F"),(-5.0,2.0,"G")]
    tree = kdtree.create(point_list=data)
    #kdtree.visualize(tree)
    list = tree.search_knn((3.0,4.0,"T"),3)
    for item in list:
        print item[0].data, item[1]
