# -*- coding: utf-8 -*-
import psycopg2
import sys, getopt



def ComputeQuery():
    global query_type
    global t_star_num 
    con = psycopg2.connect(database=database_name)
    cur = con.cursor()
    code = ""
    if query_type==0:
        code = "select count(*) from  edge as r1, edge as r2, edge as r3 where r1.edge_to=r2.edge_from and r2.edge_to=r3.edge_from and r3.edge_to=r1.edge_from and r1.edge_from!=r2.edge_from and r2.edge_from!=r3.edge_from and r1.edge_from!=r3.edge_from;"
    elif query_type==1:
        code = "select sum(count) from (select edge_from, "
        for i in range(t_star_num):
            if i==0:
                code = code+"count(*)"
            else:
                code = code+"*(count(*)-"+str(i)+")"
        code = code+"as count from edge group by edge_from) as t;"
    elif query_type==2:
        code = "Select sum(count) from (select r1.edge_from, r2.edge_to, count(*)*(count(*)-1) as count from edge as r1, edge as r2 where r1.edge_to=r2.edge_from and r1.edge_from!=r1.edge_to and r1.edge_from!=r2.edge_to group by r1.edge_from, r2.edge_to) as t;"
    else:
        code = "Select sum(count) from (select r1.edge_from, r1.edge_to, count(*)*(count(*)-1) as count from  edge as r1, edge as r2, edge as r3 where r1.edge_to=r2.edge_from and r2.edge_to=r3.edge_from and r3.edge_to=r1.edge_from and r1.edge_from!=r2.edge_from and r2.edge_from!=r3.edge_from and r1.edge_from!=r3.edge_from group by r1.edge_from, r1.edge_to) as t;;"
    cur.execute(code)
    res = int(cur.fetchone()[0])
    con.commit()
    con.close()
    print(res)
    
    

def main(argv):
    global query_type 
    query_type = 0
    global t_star_num 
    t_star_num = 3
    global database_name
    database_name = ''
    
    try:
        opts, args = getopt.getopt(argv,"h:D:T:t:",["Output=","Database=","Type=","Tstar="])
    except getopt.GetoptError:
        print("QueryResult.py -D <database> -T <Query Type:0(triangle)/1(t-star)/2(rectangle)/3(2-triangle)> -t <t-star number>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("QueryResult.py -D <database> -T <Query Type:0(triangle)/1(t-star)/2(rectangle)/3(2-triangle)> -t <t-star number>")
            sys.exit()
        elif opt in ("-D","--Database"):
            database_name = arg
        elif opt in ("-T","--Type"):
            query_type = int(arg)
        elif opt in ("-t","--Tstar"):
            t_star_num = int(arg)
        
    if query_type not in [0,1,3,2]:
        print("Invalid query type.")
        sys.exit()
    if database_name=='':
        print("Invalid database.")
        sys.exit()
        
    ComputeQuery()
    
    
    
if __name__ == "__main__":
   main(sys.argv[1:]) 
