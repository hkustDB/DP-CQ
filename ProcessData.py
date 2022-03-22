#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import getopt
import numpy



def ProcessData(input_path,out_path):
    id_dic = {}
    input_file = open(input_path,'r')
    nodes_num = 0
    for line in input_file.readlines():
        line = line.replace("\n"," ")
        nodes = line.split()
        id0 = int(nodes[0])
        id1 = int(nodes[1])
        if id0 not in id_dic.keys():
            id_dic[id0] = nodes_num
            nodes_num+=1
        if id1 not in id_dic.keys():
            id_dic[id1] = nodes_num
            nodes_num+=1    
    edges = numpy.zeros([nodes_num,nodes_num])
    input_file_t = open(input_path,'r')
    for line in input_file_t.readlines():
        line = line.replace("\n"," ")
        nodes = line.split()
        id0 = id_dic[int(nodes[0])]
        id1 = id_dic[int(nodes[1])]
        edges[id0][id1] = 1
        edges[id1][id0] = 1
    
    out_file = open(out_path,'w')
    for i in range(nodes_num):
        for j in range(nodes_num):
            if edges[i][j]==1 and i!=j:
                out_file.write(str(i)+" "+str(j)+"\n")
                


def main(argv):
    ProcessData("/Users/dongwei/Desktop/PODS/ca-Heph.txt","/Users/dongwei/Desktop/PODS/ca-HepPh_new.txt")
    


if __name__ == "__main__":
   main(sys.argv[1:])