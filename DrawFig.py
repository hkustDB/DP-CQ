# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import sys
import getopt



def ReadData():
    global file_path 
    global SS,RS,ES,QS
    dataset_name = ("CondMat","AstroPh","HepPh","HepTh","GrQc")
    query_name = ("triangle","3star","rectangle","2triangle")
    
    #ReadSS
    for i in range(5):
        for j in range(2):
            f = 3
            if j==1:
                f*=2
            input_path = file_path+"/ca-"+dataset_name[i]+"_SS_"+query_name[j]+".txt"
            input_file = open(input_path,'r')
            lines = input_file.readlines()
            for k in range(8):
                line = lines[k]
                elements =line.split()
                SS[i][j][k] = f*float(elements[2])
    #ReadRS
    for i in range(5):
        for j in range(4):
            input_path = file_path+"/ca-"+dataset_name[i]+"_RS_"+query_name[j]+".txt"
            input_file = open(input_path,'r')
            lines = input_file.readlines()
            for k in range(8):
                line = lines[k]
                elements =line.split()
                RS[i][j][k] = float(elements[2])
                
    #ReadES
    for i in range(5):
        for j in range(4):
            input_path = file_path+"/ca-"+dataset_name[i]+"_ES_"+query_name[j]+".txt"
            input_file = open(input_path,'r')
            lines = input_file.readlines()
            for k in range(8):
                line = lines[k]
                elements =line.split()
                ES[i][j][k] = float(elements[2])
                
    #ReadQS
    QS[0][0] = 1040166
    QS[1][0] = 8108646
    QS[2][0] = 20150994
    QS[3][0] = 170034
    QS[4][0] = 289560
    
    QS[0][1] = 222690360 
    QS[1][1] = 3274065312
    QS[2][1] = 7661801994
    QS[3][1] = 12590010
    QS[4][1] = 14896428
    
    QS[0][2] = 12043064
    QS[1][2] = 359332392
    QS[2][2] = 3894935680
    QS[3][2] = 1912648
    QS[4][2] = 8437784
    
    QS[0][3] = 9398600
    QS[1][3] = 289422860
    QS[2][3] = 3747561340
    QS[3][3] = 1716052
    QS[4][3] = 8165996



def main(argv):
    global file_path 
    global SS,RS,ES, QS
    file_path = ""
    pdf_file_path = ""
    try:
        opts, args = getopt.getopt(argv,"h:I:O:")
    except getopt.GetoptError:
        print("DrawFig.py -I <Input Data Path> -O <Output Path>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("DrawFig.py -I <Input Data Path> -O <Output Path>")
            sys.exit()
        if opt == '-I':
            file_path = arg
        if opt == '-O':
            pdf_file_path = arg
    
    SS = np.zeros((5,2,8))
    RS = np.zeros((5,4,8))
    ES = np.zeros((5,4,8))
    QS = np.zeros((5,4))
    ReadData()
    
    line_with = 3.5
    label_size = 18
    marker_size = 11
    marker_edge_width = 2
    legend_font_size = 25
    x_label_font_size = 27
    y_label_font_size = 27
    title_label_font_size = 27
    
    x=[0.05,0.1,0.2,0.4,0.8,1.6,3.2,6.4]
    plt.rcParams['axes.facecolor']='white'
    fig, axes = plt.subplots(5,4, figsize=(30, 33))
    
    for i in range(5):
        for j in range(4):
            axes[i,j].tick_params(axis='both', which='major', labelsize=label_size)
            if j <2:
                axes[i,j].plot(x, SS[i][j],linewidth = line_with, linestyle = '-.',label='SS',
                    marker = 's',markersize = marker_size,color=plt.cm.tab20c(12),
                    markeredgecolor=plt.cm.tab20c(12),markeredgewidth = marker_edge_width,markerfacecolor=plt.cm.tab20c(12))
            axes[i,j].plot(x, RS[i][j],linewidth = line_with,linestyle = ':',label='RS',
                marker = 'o',markersize = 8,color=plt.cm.tab20c(9),
                markeredgecolor=plt.cm.tab20c(9),markeredgewidth = marker_edge_width,markerfacecolor=plt.cm.tab20c(9))
            axes[i,j].plot(x, ES[i][j],linewidth = line_with,linestyle = '--',label='ES',
                marker = 'v',markersize = 8,color=plt.cm.tab20c(6),
                markeredgecolor=plt.cm.tab20c(6),markeredgewidth = marker_edge_width,markerfacecolor=plt.cm.tab20c(6))
            axes[i,j].axhline(y=QS[i][j],ls="-",label='Query Result',linewidth = line_with-1,markeredgecolor=plt.cm.tab20c(0))
            axes[i,j].set_yscale('log')
            axes[i,j].set_xscale('log')
    
    axes[0,0].legend(bbox_to_anchor=(0, 0.6, 1, 1),fontsize=legend_font_size,ncol=2,facecolor="white")     
    axes[0,0].set_title("Triangle counting",fontsize=title_label_font_size)
    axes[0,1].set_title("3-Star counting",fontsize=title_label_font_size)
    axes[0,2].set_title("Rectangle counting",fontsize=title_label_font_size)
    axes[0,3].set_title("2-Triangle counting",fontsize=title_label_font_size)
    
    axes[0,0].set_ylabel("CondMat",fontsize=y_label_font_size)
    axes[1,0].set_ylabel("AstroPh",fontsize=y_label_font_size)
    axes[2,0].set_ylabel("HepPh",fontsize=y_label_font_size)
    axes[3,0].set_ylabel("HepTh",fontsize=y_label_font_size)
    axes[4,0].set_ylabel("GrQc",fontsize=y_label_font_size)
    
    axes[4,0].set_xlabel(u"value of \u03B2",fontsize=x_label_font_size)
    axes[4,1].set_xlabel(u"value of \u03B2",fontsize=x_label_font_size)
    axes[4,2].set_xlabel(u"value of \u03B2",fontsize=x_label_font_size)
    axes[4,3].set_xlabel(u"value of \u03B2",fontsize=x_label_font_size)  
    plt.savefig(pdf_file_path)  
    
    

if __name__ == "__main__":
   main(sys.argv[1:])    