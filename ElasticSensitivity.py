#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import psycopg2
import sys, getopt
import math



def GetDegree():
    global database_name
    global degree
    con = psycopg2.connect(database=database_name)
    cur = con.cursor()
    code = "select max(count) from (select edge_from, count(*) from edge group by edge_from) as t;"
    cur.execute(code)
    degree = int(cur.fetchone()[0])
    con.commit()
    con.close()
    
    
    
def ComputeS(t,mf):
    if t==1:
        return 1
    return math.pow(mf,t-1)+(mf+1)*ComputeS(t-1,mf)
    
    
    
def ComputeESTriangle(beta):
    global degree
    res = 0
    for i in range(10000):
        ls_i = ComputeS(3,degree+i)*pow(math.e,-1*beta*i)
        if res<ls_i:
            res = ls_i
    return res



def ComputeESTStar(beta,t_star_num):
    global degree
    res = 0
    for i in range(10000):
        ls_i = ComputeS(t_star_num,degree+i)*pow(math.e,-1*beta*i)
        if res<ls_i:
            res = ls_i
    return res
    
    

def ComputeESRectangle(beta):
    global degree
    res = 0
    for i in range(10000):
        ls_i = ComputeS(4,degree+i)*pow(math.e,-1*beta*i)
        if res<ls_i:
            res = ls_i
    return res



def ComputeES2Triangle(beta):
    global degree
    res = 0
    for i in range(10000):
        ls_i = ComputeS(5,degree+i)*pow(math.e,-1*beta*i)
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
            res = ComputeESTriangle(beta)
        elif query_type==1:
            res = ComputeESTStar(beta,t_star_num)
        elif query_type==2:
            res = ComputeESRectangle(beta)
        else:
            res = ComputeES2Triangle(beta)
        output_file.write(str(i+1)+" "+str(beta)+" "+str(res)+"\n")
    
    

def main(argv):
    global output_path 
    output_path = ''
    global query_type 
    query_type = 0
    global t_star_num 
    t_star_num = 3
    global database_name
    database_name = ''
    
    try:
        opts, args = getopt.getopt(argv,"h:O:D:T:t:",["Output=","Database=","Type=","Tstar="])
    except getopt.GetoptError:
        print("ElasticSensitivity.py -O <output> -D <database> -T <Query Type:0(triangle)/1(t-star)/2(rectangle)/3(2-triangle)> -t <t-star number>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("ElasticSensitivity.py -O <output> -D <database> -T <Query Type:0(triangle)/1(t-star)/2(rectangle)/3(2-triangle)> -t <t-star number>")
            sys.exit()
        elif opt in ("-O", "--Output"):
            output_path = arg
        elif opt in ("-D","--Database"):
            database_name = arg
        elif opt in ("-T","--Type"):
            query_type = int(arg)
        elif opt in ("-t","--Tstar"):
            t_star_num = int(arg)
        
    if output_path=='':
        print("Invalid output path.")
        sys.exit()
    if query_type not in [0,1,3,2]:
        print("Invalid query type.")
        sys.exit()
    if database_name=='':
        print("Invalid database.")
        sys.exit()
        
    GetDegree()
    Compute()
    
    

if __name__ == "__main__":
   main(sys.argv[1:])    