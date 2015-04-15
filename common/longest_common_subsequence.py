#!/usr/bin/env python
# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from shingling import drop_symbol


class LongestCommonSubsequence():
    def __init__(self, str_x, str_y):
        # init array c and array b
        # c[i,j]为序列Xi和Yj的一个LCS长度
        # b[i,j]为一个向量数组
        self.str_x = str_x.decode("utf-8")
        self.str_y = str_y.decode("utf-8")
        self.c = [[0 for col in range(len(self.str_y) + 1)] for row in range(len(self.str_x) + 1)]
        self.b = [[0 for col in range(len(self.str_y) + 1)] for row in range(len(self.str_x) + 1)]
        self.lcs = []
        self.lcs_init()

    # init longest common subsequence's length
    def lcs_init(self):
        m = len(self.str_x) + 1
        n = len(self.str_y) + 1
        for i in range(1, m):
            for j in range(1, n):
                if self.str_x[i-1] == self.str_y[j-1]:
                    self.c[i][j] = self.c[i-1][j-1] + 1
                    self.b[i][j] = "-1,-1"
                else:
                    if self.c[i-1][j] >= self.c[i][j-1]:
                        self.c[i][j] = self.c[i-1][j]
                        self.b[i][j] = "-1,0"
                    else:
                        self.c[i][j] = self.c[i][j-1]
                        self.b[i][j] = "0,-1"

    def get_cls(self):
        self.recursive_lcs(len(self.str_x), len(self.str_y))
        return self.lcs

    def recursive_lcs(self, i, j):
        #print i, j
        if i == 0 or j == 0:
            return 0
        vector_array = self.parse_vector(self.b[i][j])
        if vector_array == (-1,-1):
            self.recursive_lcs(i+vector_array[0], j+vector_array[1])
            self.lcs.append(self.str_x[i-1])
        else:
            self.recursive_lcs(i+vector_array[0], j+vector_array[1])

    def parse_vector(self, vector_str):
        vector = vector_str.split(",")
        return (int(vector[0]), int(vector[1]))




def max_length(str_x, str_y):
    str_x = str_x.decode("utf-8")
    str_y = str_y.decode("utf-8")
    len_x = len(str_x)
    len_y = len(str_y)
    if len_x > len_y:
        return len_x
    else:
        return len_y

def longest_common_subsequence_percentage(str_x, str_y):
    if not str_x or not str_y:
        return 0.0
    str_x = drop_symbol(str_x)
    str_y = drop_symbol(str_y)
    lcs = LongestCommonSubsequence(str_x, str_y)
    list = lcs.get_cls()
    return float(len(list)) / max_length(str_x, str_y)


if __name__ == "__main__":
    str_x = "北京如家大酒店"
    str_y = "北京酒仙桥如家酒店"
    lcs = LongestCommonSubsequence(str_x, str_y)
    list = lcs.get_cls()
    print len(list)
    for item in list:
        print item

    print longest_common_subsequence_percentage(str_x, str_y)
