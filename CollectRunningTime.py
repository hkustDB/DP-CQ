# -*- coding: utf-8 -*-
import sys
import os
import psycopg2
import getopt
import time



def TestRunningTime():
    global work_path 
    global query_id
    global data_id
    dataset_name = ("CondMat","AstroPh","HepPh","HepTh","GrQc")
    query_name = ("triangle","3star","rectangle","2triangle")
    
    repeat_time = 10
    time_Q = 0
    time_SS = 0
    time_ES = 0
    time_RS = 0
    for i in range(repeat_time):
        
        if query_id<2:
            start = time.time()
            cmd = work_path+"python "+work_path+"/SmoothSensitivity.py -I "+work_path+"/ca-"+dataset_name[data_id]+"_new.txt -T "+str(query_id)+" -O "+work_path+"/hehe.txt" 
            shell = os.popen(cmd, 'r')
            shell.close()
            end= time.time()
            time_SS+=(end-start)
        start = time.time()
        cmd = work_path+"python "+work_path+"/QueryResult.py -D "+dataset_name[data_id]+" -T "+str(query_id)   
        shell = os.popen(cmd, 'r')
        shell.close()
        end= time.time()
        time_Q+=(end-start)
        
        
        
        start = time.time()
        cmd = work_path+"python "+work_path+"/ElasticSensitivity.py -O "+work_path+"/hehe.txt -D "+dataset_name[data_id]+" -T "+str(query_id)   
        shell = os.popen(cmd, 'r')
        shell.close()
        end= time.time()
        time_ES+=(end-start)
        
        start = time.time()
        cmd = work_path+"python "+work_path+"/ResidualSensitivity.py -O "+work_path+"/hehe.txt -D "+dataset_name[data_id]+" -T "+str(query_id)   
        shell = os.popen(cmd, 'r')
        shell.close()
        end= time.time()
        time_RS+=(end-start)
        
    if query_id<2:
        print("Time for SS")
        print(time_SS/repeat_time+time_Q/repeat_time)
        print("Time for RS")
        print(time_RS/repeat_time+time_Q/repeat_time)
        print("Time for ES")
        print(time_ES/repeat_time+time_Q/repeat_time)
        print("Time for SS/RS")
        print((time_SS+time_Q)/(time_RS+time_Q))
        print("Time for RS/ES")
        print((time_RS+time_Q)/(time_ES+time_Q))
    else:
        print("Time for RS")
        print(time_RS/repeat_time+time_Q/repeat_time)
        print("Time for ES")
        print(time_ES/repeat_time+time_Q/repeat_time)
        print("Time for RS/ES")
        print((time_RS+time_Q)/(time_ES+time_Q))
    


def main(argv):
    global work_path 
    global query_id
    global data_id
    work_path = ""
    try:
        opts, args = getopt.getopt(argv,"h:I:Q:d:")
    except getopt.GetoptError:
        print("CollectRunningTime.py -I <Input Data Path> -Q <Query> -d <dataset>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("CollectRunningTime.py -I <Input Data Path> -Q <Query> -d <dataset>")
            sys.exit()
        if opt == '-I':
            work_path = arg
        if opt == '-Q':
            query_id = int(arg)
        if opt == '-d':
            data_id = int(arg)
    
    TestRunningTime()
            


if __name__ == "__main__":
   main(sys.argv[1:]) 