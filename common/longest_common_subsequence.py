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

    # init longest common subsequence's length
    def lcs_init(self):
        self.c = [[0 for col in range(len(self.str_y) + 1)] for row in range(len(self.str_x) + 1)]
        self.b = [[0 for col in range(len(self.str_y) + 1)] for row in range(len(self.str_x) + 1)]
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

    # if only want to get longest common subsequence's length, use this method to init
    # because only to get length, so use array c's 2 row is enough
    def lcs_length_init(self):
        self.length = [[0 for col in range(len(self.str_y) + 1)] for row in range(2)]
        m = len(self.str_x) + 1
        n = len(self.str_y) + 1
        for i in range(1, m):
            for j in range(1, n):
                index = self.cls_length_row(i)
                if self.str_x[i-1] == self.str_y[j-1]:
                    self.length[index[0]][j] = self.length[index[1]][j-1] + 1
                else:
                    if self.length[index[1]][j] >= self.length[index[0]][j-1]:
                        self.length[index[0]][j] = self.length[index[1]][j]
                    else:
                        self.length[index[0]][j] = self.length[index[0]][j-1]

    # get longest common subsequence's length
    def get_cls_length(self):
        self.lcs_length_init()
        index = self.cls_length_row(len(self.str_x))
        return self.length[index[0]][-1]

    # get longest common subsequence
    def get_cls(self):
        # init array b and array c
        self.lcs_init()
        # use cls to store longest common subsequence
        self.lcs = []
        self.recursive_lcs(len(self.str_x), len(self.str_y))
        return self.lcs

    # store longest common subsequence's value
    def recursive_lcs(self, i, j):
        if i == 0 or j == 0:
            return 0
        vector_array = self.parse_vector(self.b[i][j])
        if vector_array == (-1,-1):
            self.recursive_lcs(i+vector_array[0], j+vector_array[1])
            self.lcs.append(self.str_x[i-1])
        else:
            self.recursive_lcs(i+vector_array[0], j+vector_array[1])

    # parse array b's vector
    def parse_vector(self, vector_str):
        vector = vector_str.split(",")
        return (int(vector[0]), int(vector[1]))

    # cross to use 2 rows: when only want to get cls's length
    def cls_length_row(self, i):
        return (i%2, (i%2)^1)


def max_length(str_x, str_y):
    str_x = str_x.decode("utf-8")
    str_y = str_y.decode("utf-8")
    if len(str_x) > len(str_y):
        return len(str_x)
    else:
        return len(str_y)

def longest_common_subsequence_percentage(str_x, str_y):
    if not str_x or not str_y:
        return 0.0
    str_x = drop_symbol(str_x)
    str_y = drop_symbol(str_y)
    lcs = LongestCommonSubsequence(str_x, str_y)
    length = lcs.get_cls_length()
    return float(length) / max_length(str_x, str_y)


if __name__ == "__main__":
    str_x = 'ABCBDAB'
    str_y = 'BDCABA'
    print longest_common_subsequence_percentage(str_x, str_y)
    #lcs = LongestCommonSubsequence(str_x, str_y)
    #print lcs.get_cls_length()
    #list = lcs.get_cls()
    #for item in list:
    #    print item
