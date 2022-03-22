# -*- coding: utf-8 -*-
import sys, getopt, math
import numpy



def ReadData():
    global a
    global b
    global c
    global query_type 
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
    degree = numpy.zeros(nodes_num)
    for line in input_file_t.readlines():
        line = line.replace("\n"," ")
        nodes = line.split()
        id0 = id_dic[int(nodes[0])]
        id1 = id_dic[int(nodes[1])]
        edges[id0][id1] = 1
        edges[id1][id0] = 1
        degree[id0]+=1
        
    a = []
    b = []
    c = []
    
    if query_type==0:
        matrix_res = numpy.dot(edges,edges)
        a_dic = {}
        for i in range(nodes_num):
            for j in range(nodes_num):
                if i==j:
                    continue
                a_t = matrix_res[i][j]
                b_t = degree[i]+degree[j]-2*a_t
                
                if a_t not in a_dic.keys():
                    a_dic[a_t] = b_t
                elif b_t>a_dic[a_t]:
                    a_dic[a_t] = b_t
        for a_t in a_dic.keys():
            a.append(a_t)
            b.append(a_dic[a_t])
    else:
        for i in range(nodes_num):
            degree_t = degree[i]
            c.append(degree_t)
        
    
    
def ComputeSSTriangle(beta):
    global b
    global a
    res = 0
    for i in range(10000):
        ls_i = 0
        for j in range(len(a)):
            ls_i_t = a[j]+ int((i+min(i,b[j]))*1.0/2)
            if ls_i_t>ls_i:
                ls_i = ls_i_t
        ls_i = ls_i*pow(math.e,-1*beta*i)
        if res<ls_i:
            res = ls_i
    return res
    


def fac(a,k):
    res = 1
    for i in range(k):
        res*=(a-i)
    return res



def ComputeSSTStar(beta,t):
    global c
    res = 0
    max_c = max(c)
    for i in range(int(t*100000)):
        ls_i = fac(max_c+i,t-1)/fac(t-1,t-1)*pow(math.e,-1*beta*i)
        if res<ls_i:
            res = ls_i
    return res



def Compute():
    global query_type 
    global output_path 
    global t_star_num 
    output_file = open(output_path ,'w')
    
    for i in range(9):
        beta = 0.05*math.pow(2,i)
        res = 0
        if query_type==0:
            res = ComputeSSTriangle(beta)
        else:
            res = ComputeSSTStar(beta,t_star_num)
        output_file.write(str(i+1)+" "+str(beta)+" "+str(res)+"\n")
    


def main(argv):
    global input_path 
    input_path = ''
    global output_path 
    output_path = ''
    global query_type 
    query_type = 0
    global t_star_num 
    t_star_num = 3
    
    try:
        opts, args = getopt.getopt(argv,"h:I:O:T:t:",["Input=","Output=","Type=","Tstar="])
    except getopt.GetoptError:
        print("SmoothSensitivity.py -I <input> -O <out> -T <Query Type:0(triangle)/1(t-star)> -t <t-star number>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("SmoothSensitivity.py -I <input> -O <out> -T <Query Type:0(triangle)/1(t-star)> -t <t-star number>")
            sys.exit()
        elif opt in ("-I", "--Input"):
            input_path = arg
        elif opt in ("-O","--Output"):
            output_path = arg
        elif opt in ("-T","--Type"):
            query_type = int(arg)
        elif opt in ("-t","--Tstar"):
            t_star_num = int(arg)
    
    if input_path=='':
        print("Invalid input path.")
        sys.exit()
    if output_path=='':
        print("Invalid output path.")
        sys.exit()
    if query_type not in [0,1]:
        print("Invalid query type.")
        sys.exit()
        
    ReadData()
    Compute()
    

if __name__ == "__main__":
   main(sys.argv[1:])    
