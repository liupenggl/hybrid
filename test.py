#-*- coding:utf-8 -*-
from scipy import stats
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from gfile import *
import networkx as nx
import random
import string 

from prandom import *
from rsel import *
from kanonymity import *



def test_il_k():
    g=nx.Graph()
    #filepath=r'\newmovies.txt'
  
    filepath=r'\citation-raw.txt'
    #filepath=r'\polbooks.txt'
    filepath=os.getcwd()+r'\data'+ filepath
    read_file_txt(g,path=filepath)

    tempname=os.path.split(filepath)
    outName=os.getcwd()+r'\data\result\il_'+tempname[1]
    f=open(outName,'w')
    h=nx.Graph(g)

    for k in range(5,45,5):
        h=nx.Graph(g)
        f.write('k={0:>3} il={1:>3}\n'.format(k,k_anonymity(g,k)*3))

    f.close()  



def test_subrisk():
    g=nx.Graph()
    #filepath=r'D:\program\data\partialkanonmity\newmovies.txt'
    filepath=r'\polbooks.txt'
    #filepath=r'D:\program\data\partialkanonmity\citation-raw.txt'
    filepath=os.getcwd()+r'\data'+ filepath
    read_file_txt(g,path=filepath)

    tempname=os.path.split(filepath)
    outName=os.getcwd()+r'\data\p_'+tempname[1]
    f=open(outName,'w')
    for k in range(5,45,5):     
        vk,vr=partition(g,k)
        m=20
        p=1.0/k
        r=subrisk(g,vr,m)
        mMax=len(g.subgraph(vr).edges())
        while r>p:
            m=m+5
            r=r=subrisk(g,vr,m)
            f.write('k={0} m={1} r={2}\n'.format(k, m, r))
            if m>mMax:
                break
        f.write('k={0},r={1},m={2}\n'.format(k,r,m))
     
    f.close()  



def test1():
    g=nx.Graph()
    filepath=r'D:\program\code\hybrid\data\graph.txt'
    read_file_txt(g,path=filepath)
    sh(g)

if __name__=="__main__":
    print 'sss'
    #test_subrisk()
    test_il_k()