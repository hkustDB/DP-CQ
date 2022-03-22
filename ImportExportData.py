# -*- coding: utf-8 -*-
import psycopg2
import sys, getopt



def main(argv):
    input_path = ''
    database_name = ''
    model = 0
    
    try:
        opts, args = getopt.getopt(argv,"h:I:D:m:",["Input=","Database=","Model="])
    except getopt.GetoptError:
        print("ImportExportData.py -I <input> -D <database name> -m <model:0(import)/1(export)>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("ImportExportData.py -I <input> -D <database name> -m <model:0(import)/1(export)>")
            sys.exit()
        elif opt in ("-I", "--Input"):
            input_path = arg
        elif opt in ("-D","--Database"):
            database_name = arg
        elif opt in ("-m","--Model"):
            model = int(arg)
            
    if model not in [0,1]:
        print("Invalid query type.")
        sys.exit()
    if database_name=='':
        print("Invalid database.")
        sys.exit()
    if model == 0:
        if input_path=='':
            print("Invalid input path.")
            sys.exit()
        
    con = psycopg2.connect(database=database_name)
    cur = con.cursor()
    
    if model==0:
        code = "CREATE TABLE EDGE (EDGE_FROM INTEGER NOT NULL,EDGE_TO INTEGER NOT NULL);"
        cur.execute(code)
        code = "Copy edge FROM '"+input_path+"' WITH DELIMITER AS ' ';"
        cur.execute(code)
    else:
        code = "drop table edge;"

    con.commit()
    con.close()
    
    
    
if __name__ == "__main__":
   main(sys.argv[1:])
