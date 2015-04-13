#!/usr/bin/python
# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def shing_str(pre_str,cmp_str):
    if not pre_str or not cmp_str:
        return 0.0
    pre_vec=set();cmp_vec=set()
    pre_str=drop_symbol(pre_str)
    cmp_str=drop_symbol(cmp_str)
    try:
        pre_str=pre_str.decode("utf-8")
        cmp_str=cmp_str.decode("utf-8")
    except:
        return 0.0
    i=0;j=0
    while(i<len(pre_str)-1):
        pre_vec.add(pre_str[i]+pre_str[i+1])
        i=i+1
    while(j<len(cmp_str)-1):
        cmp_vec.add(cmp_str[j]+cmp_str[j+1])
        j=j+1
    comNum=allNum=0.0
    for k in pre_vec:
        if k in cmp_vec:
            comNum+=1
    allNum=len(pre_vec)+len(cmp_vec)
    if allNum:
        return comNum/(allNum-comNum)
    else:
        return 0.0
def drop_symbol(s):
    blackSet=set(["▪","●",".","–","(",")"," ","\t","（","）","-","?",",","，","•","·"])
    for sym in blackSet:
        s=s.replace(sym,"")
    return s
if __name__=="__main__":
    a="北京如家酒店"
    b="北京酒仙桥如家酒店"
    print shing_str(a,b)

