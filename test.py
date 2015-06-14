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

def clustering(g, nodes=None, weight=None):      
    if g.is_directed():
        raise NetworkXError('Clustering algorithms are not defined ',
                            'for directed graphs.')
    if weight is not None:
        td_iter=_weighted_triangles_and_degree_iter(g,nodes,weight)
    else:
        td_iter=_triangles_and_degree_iter(g,nodes)

    clusterc={}

    for v,d,t in td_iter:
        if t==0:
            clusterc[v]=0.0
        else:
            clusterc[v]=t/float(d*(d-1))

    if nodes in g: 
        return list(clusterc.values())[0] # return single value
    return clusterc

def test_cc():
    g=nx.Graph()
    #filepath=r'D:\program\data\partialkanonmity\newmovies.txt'
    filepath=r'D:\program\data\partialkanonmity\polbooks.txt'
    #filepath=r'D:\program\data\partialkanonmity\citation-raw.txt'
    read_file_txt(g,path=filepath)
    tempname=os.path.split(filepath)
    outName=os.getcwd()+r'\data\cc_'+tempname[1]
    f=open(outName,'w')

    print nx.clustering(g)

    f.close()  

def test_subrisk():
    g=nx.Graph()
    #filepath=r'D:\program\data\partialkanonmity\newmovies.txt'
    filepath=r'D:\program\data\partialkanonmity\polbooks.txt'
    #filepath=r'D:\program\data\partialkanonmity\citation-raw.txt'
    read_file_txt(g,path=filepath)
    tempname=os.path.split(filepath)
    outName=os.getcwd()+r'\data\p_'+tempname[1]
    f=open(outName,'w')
    for k in range(25,45,5):     
        vk,vr=p_kann(g,k)
        m=20
        p=1.0/k
        r=subrisk(g,vr,m)
        mMax=len(g.subgraph(vr).edges())
        while r>p:
            m=m+2
            r=r=subrisk(g,vr,m)
            f.write('k={0} m={1} r={2}\n'.format(k, m, r))
            if m>mMax:
                break
        f.write('k={0},r={1},m={2}\n'.format(k,r,m))
     
    f.close()  

def test_il_p():
    g=nx.Graph()
    #filepath=r'D:\program\data\partialkanonmity\newmovies.txt'
    filepath=r'D:\program\data\partialkanonmity\polbooks.txt'
    #filepath=r'D:\program\data\partialkanonmity\citation-raw.txt'
    read_file_txt(g,path=filepath)
    tempname=os.path.split(filepath)
    outName=os.getcwd()+r'\data\p_'+tempname[1]
    f=open(outName,'w')


    f.close()  


def test1():
    g=nx.Graph()
    filepath=r'D:\program\code\hybrid\data\graph.txt'
    read_file_txt(g,path=filepath)
    sh(g)

if __name__=="__main__":
    print 'sss'
    #test_subrisk()
    test_cc()