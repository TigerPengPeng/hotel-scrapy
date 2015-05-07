#!/usr/bin/python
# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def shingling_value(str_x, str_y, w):
    if not str_x or not str_y:
        return 0.0
    str_x = str_x.decode("utf-8")
    str_y = str_y.decode("utf-8")
    m = len(str_x)
    n = len(str_y)
    X = set()
    Y = set()
    for i in range(0, m-w+1):
        sub_c = []
        for k in range(i, i+w):
            sub_c.append(str_x[k])
        X.add("".join(sub_c))
    for i in range(0, n-w+1):
        sub_c = []
        for k in range(i, i+w):
            sub_c.append(str_y[k])
        Y.add("".join(sub_c))
    common = 0.0
    for item in X:
        if item in Y:
            common += 1
    return common / (len(X) + len(Y) - common)


if __name__ == "__main__":
    str_x = "北京如家酒店"
    str_y = "北京酒仙桥如家酒店"
    print shingling_value(str_x, str_y, 2)
