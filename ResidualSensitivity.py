#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import psycopg2
import sys, getopt, math
import numpy as np



def CollectTEQ1():
    global TE
    con = psycopg2.connect(database=database_name)
    cur = con.cursor()
    code = "select max(count) from (select r1.edge_from, r2.edge_to, count(*) from edge as r1, edge as r2 where r1.edge_to=r2.edge_from and r1.edge_from!=r1.edge_to and r1.edge_from!=r2.edge_to group by r1.edge_from, r2.edge_to) as t;"
    cur.execute(code)
    r1 = int(cur.fetchone()[0])
    TE = np.ones(8)
    TE[0b110] = r1
    TE[0b101] = r1
    TE[0b011] = r1
    con.commit()
    con.close()
    
    
    
def Fac(a,k):
    res = 1
    for i in range(k):
        res*=(a-i)
    return res



def NumberOfOnes(num):
    if num==0:
        return 0
    return num%2+NumberOfOnes(int(num/2))


    
def CollectTEQ2():
    global TE
    global t_star_num 
    con = psycopg2.connect(database=database_name)
    cur = con.cursor()
    code = "select max(count) from (select edge_from, count(*) from edge group by edge_from) as t;"
    cur.execute(code)
    r1 = float(cur.fetchone()[0])
    size_TE = int(math.pow(2,t_star_num))
    TE = np.ones(size_TE)
    for i in range(1,t_star_num):
        res = Fac(r1,i)
        for j in range(size_TE): 
            if NumberOfOnes(j)==i:
                TE[j] = res
    con.commit()
    con.close()
    


def CollectTEQ3():
    global TE
    con = psycopg2.connect(database=database_name)
    cur = con.cursor()
    code = "select max(count) from (select r1.edge_from, r2.edge_to, count(*) from edge as r1, edge as r2 where r1.edge_to=r2.edge_from and r1.edge_from!=r1.edge_to and r1.edge_from!=r2.edge_to group by r1.edge_from, r2.edge_to) as t;"
    cur.execute(code)
    r1 = int(cur.fetchone()[0])
    code = "create table t1 as (select r1.edge_from, r2.edge_to, count(*) from edge as r1, edge as r2 where r1.edge_to=r2.edge_from and r1.edge_from!=r1.edge_to and r1.edge_from!=r2.edge_to group by r1.edge_from, r2.edge_to);"
    cur.execute(code)
    code = "select max(sum) from (select t1.edge_from, edge.edge_to, sum(count-1) from t1, edge where t1.edge_to=edge.edge_from and t1.edge_from!=edge.edge_to group by t1.edge_from, edge.edge_to) as t;"
    cur.execute(code)
    r2 = int(cur.fetchone()[0])
    code = "drop table t1;"
    cur.execute(code)
    TE = np.ones(16)
    TE[0b1100] = r1
    TE[0b1001] = r1
    TE[0b0110] = r1
    TE[0b0101] = r1
    TE[0b0011] = r1
    
    TE[0b1110] = r2
    TE[0b1101] = r2
    TE[0b1011] = r2
    TE[0b0111] = r2
    con.commit()
    con.close()
    
    
    
def CollectTEQ4():
    global TE
    TE = np.ones(32)
    con = psycopg2.connect(database=database_name)
    cur = con.cursor()
    code = "select max(count) from (select r1.edge_from, r2.edge_to, count(*) from edge as r1, edge as r2 where r1.edge_to=r2.edge_from and r1.edge_from!=r1.edge_to and r1.edge_from!=r2.edge_to group by r1.edge_from, r2.edge_to) as t;"
    cur.execute(code)
    r1 = int(cur.fetchone()[0])
    r2 = r1
    code = "select max(count) from (select r1.edge_from, r1.edge_to, count(*) from  edge as r1, edge as r2, edge as r3 where r1.edge_to=r2.edge_from and r2.edge_to=r3.edge_from and r3.edge_to=r1.edge_from and r1.edge_from!=r2.edge_from and r2.edge_from!=r3.edge_from and r1.edge_from!=r3.edge_from group by r1.edge_from, r1.edge_to) as t;"
    cur.execute(code)
    r3 = int(cur.fetchone()[0])
    
    limit_num = 1000
    r4=1
    r5=0
    while r4>r5:
        code = "Create table t1 as (select r1.edge_from, r2.edge_to, count(*) from edge as r1, edge as r2 where r1.edge_to=r2.edge_from and r1.edge_from!=r1.edge_to and r1.edge_from!=r2.edge_to group by r1.edge_from, r2.edge_to order by count desc limit "+str(limit_num)+");"
        cur.execute(code)
        code = "Select min(count) from t1;"
        cur.execute(code)
        r4 = int(cur.fetchone()[0])
        code = "select max(count) from (select r1.edge_to, r2.edge_to, r3.edge_to, count(*) from t1, edge as r1, edge as r2, edge as r3 where r1.edge_from=r2.edge_from and r1.edge_from=r3.edge_from and r1.edge_from!=r1.edge_to and r1.edge_from!=r2.edge_to and r1.edge_from!=r3.edge_to and  r1.edge_to!=r2.edge_to and r1.edge_to!=r3.edge_to and r2.edge_to!=r3.edge_to and t1.edge_from =r1.edge_to and t1.edge_to =r2.edge_to group by r1.edge_to, r2.edge_to, r3.edge_to) as t;"
        cur.execute(code)
        r5 = int(cur.fetchone()[0])
        code = "Drop table t1;"
        cur.execute(code)
        limit_num*=10
    code = "Select max(count) from (select r1.edge_from, r2.edge_to, count(*)*(count(*)-1) as count from edge as r1, edge as r2 where r1.edge_to=r2.edge_from and r1.edge_from!=r1.edge_to and r1.edge_from!=r2.edge_to group by r1.edge_from, r2.edge_to) as t;"
    cur.execute(code)
    r6 = int(cur.fetchone()[0])
    
    code = "Create table t1 as (select r1.edge_from, r1.edge_to, count(*)-1 as count from  edge as r1, edge as r2, edge as r3 where r1.edge_to=r2.edge_from and r2.edge_to=r3.edge_from and r3.edge_to=r1.edge_from and r1.edge_from!=r2.edge_from and r2.edge_from!=r3.edge_from and r1.edge_from!=r3.edge_from group by r1.edge_from, r1.edge_to);"
    cur.execute(code)
    code = "select max(sum) from (Select t1.edge_from, edge.edge_to, sum(count) from edge, t1 where edge.edge_from=t1.edge_to and edge.edge_to!=t1.edge_to and edge.edge_to!=t1.edge_from group by t1.edge_from, edge.edge_to) as t;"
    cur.execute(code)
    r7 = int(cur.fetchone()[0])
    code = "Drop table t1;"
    cur.execute(code)
    TE[0b11000] = r1
    TE[0b00110] = r1
    
    TE[0b11100] = r2
    TE[0b11010] = r2
    TE[0b10110] = r2
    TE[0b01110] = r2
    
    TE[0b11001] = r3
    TE[0b00111] = r3
    
    TE[0b10011] = r5
    TE[0b01101] = r5

    TE[0b11110] = r6
    
    TE[0b11101] = r7
    TE[0b11011] = r7
    TE[0b10111] = r7
    TE[0b01111] = r7



def CollectTE():
    global query_type 
    if query_type==0:
        CollectTEQ1()
    elif query_type==1:
        CollectTEQ2()
    elif query_type==2:
        CollectTEQ3()
    elif query_type==3:
        CollectTEQ4()
        


def BinToInt(bin_num, size):
    res = 0
    for i in range(size):
        res+=pow(2,size-1-i)*bin_num[i]
    return int(res)



def IntToBin(int_num,size):
    bin_num = np.zeros(size)
    for i in range(size):
        bin_num[size-1-i] = int_num%2
        int_num = int(int_num/2)
    return bin_num



def RecCompHatTE(cur_i,table_num,ori_TE,cur_TE,num_k,k):
    global TE
    if cur_i==table_num:
        int_num = BinToInt(cur_TE,table_num)
        #Let 0^0=1
        if num_k==0:
            return TE[int_num]
        else:
            return TE[int_num]*math.pow(k,num_k)
    if ori_TE[cur_i]==0:
        cur_TE[cur_i]=0
        return RecCompHatTE(cur_i+1,table_num,ori_TE,cur_TE,num_k,k)
    else:
        cur_TE[cur_i]=1
        r1=RecCompHatTE(cur_i+1,table_num,ori_TE,cur_TE,num_k,k)
        cur_TE[cur_i]=0
        r2=RecCompHatTE(cur_i+1,table_num,ori_TE,cur_TE,num_k+1,k)
        return r1+r2
        


def ComputeRS(beta):
    global TE
    global table_num
    res = 0
    max_k = int(table_num*1.1/beta)
    max_k = max(1,max_k)
        
    for k in range(max_k):
        #Compute TE first
        hat_TE = np.zeros(pow(2,table_num))
        for i in range(int(pow(2,table_num))):
            bin_num = IntToBin(i,table_num)
            new_bin_num = np.zeros(table_num)
            hat_TE[i] = RecCompHatTE(0,table_num,bin_num,new_bin_num,0,k)
        ls_i = 0
        for i in range(int(pow(2,table_num))-1):
            ls_i+=hat_TE[i]
        ls_i*=pow(math.e,-1*beta*k)
        if res<ls_i:
            res = ls_i
    return res
            


def Compute():
    global query_type 
    global output_path 
    global t_star_num 
    global table_num
    output_file = open(output_path ,'w')
    
    table_num = 0
    if query_type==0:
        table_num = 3
    elif query_type==1:
        table_num = t_star_num
    elif query_type==2:
        table_num = 4
    elif query_type==3:
        table_num = 5
    

    for i in range(9):
        beta = 0.05*math.pow(2,i)
        res = ComputeRS(beta)
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
        print("ResidualSensitivity.py -O <output> -D <database> -T <Query Type:0(triangle)/1(t-star)/2(rectangle)/3(2-triangle)> -t <t-star number>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("ResidualSensitivity.py -O <output> -D <database> -T <Query Type:0(triangle)/1(t-star)/2(rectangle)/3(2-triangle)> -t <t-star number>")
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
    
    CollectTE()
    Compute()
    
    
    
if __name__ == "__main__":
   main(sys.argv[1:])    
