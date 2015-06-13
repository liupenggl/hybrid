#-*- coding:utf-8 -*-
from scipy import stats
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from gfile import *
import networkx as nx
import random
import string 

import os

def del_edge(g,m):
    """remove m edges in g at random"""
    if len(g.edges())>=m:
            medge=random.sample(g.edges(),m)
            return medge
    else:
        print "not enough edges to remove, please check m"

def add_edge(g,m):
    compl=nx.complement(g)
    if len(compl.edges())>=m:
        aedge=random.sample(compl.edges(),m)
        return aedge
    else:
        print "not enough nodes to add m edges, please check m"
def p_kann(g,k):
    """vk 包含节满足k匿名，vr包含节点不满足k匿名"""
    if not g.nodes():
        print "In p_kann(g,k) g is empty!"
        return 0
    vr=[]
    vk=[]
    d=g.degree().items()
    dh=nx.degree_histogram(g)

    for each in d:
        if dh[each[1]]<k:
            vr.append(each[0])
        else:
            vk.append(each[0])

    return vk,vr

def binomial_con_di(z,node,g,m):
    """删除m条边 X，然后添加m条边Y，z 是节点的度，node节点的标签，g图
    """
    if z<0:
        return 0
    n1=m if m<len(g[node]) else len(g[node])#delete at most min(m,node degree) edges, because a node has only len(g[node]) edges
    p1=1.0*m/len(g.edges())# n1 trails whit deleting probality p1
    
    n2=m if m<(len(g.edges())-1-len(g[node])) else (len(g.edges())-1-len(g[node]))#leave enough node for edges adding
    p2=1.0*m/(len(g.nodes())*(len(g.nodes())-1)/2)

    di=len(g[node])
    sum=0.0
    t=0
    while t<=n1:
        if z-di+t>=0 and z-di+t<=n2:
            sum=sum+stats.binom.pmf(t,n1,p1)*stats.binom.pmf(z-di+t,n2,p2)#adding z-di edges

        t+=1
    return sum


def vrisk(node,g,subli,m=2):
    """
    return the probability of the node can be reidentfy by m pertubation
    """

    subg=g.subgraph(subli)
    ddiff=len(g[node])-len(subg[node])
    pr=binomial_con_di(len(g[node])-ddiff,node,subg,m)#the prob of the degree of node not change.
    #print node
    #print pr

    prr=1-pr
    #f=open("temp.txt",'w')
    
    for each in subli:
        ddiff=len(g[each])-len(subg[each])
        #f.write('{0:>2} {1} {2} {3}'.format(each,' : ',binomial_con_di(len(g[node])-ddiff,each,subg,m),'\n'))
        prr=prr+binomial_con_di(len(g[node])-ddiff,each,subg,m)

    return pr*(1.0/prr) 
    #f.close()

def subrisk(g,subli,m=2):
    max=0
    f=open("temp.txt",'w')

    for each in subli:
        temp=vrisk(each,g,subli,m)
        #f.write('{0:>2} {1} {2} {3}'.format(each,' : ',vrisk(each,g,subli,m),'\n'))
        max=max if max>temp else temp

    f.close()
    print max
    return max

def test_subrisk():
    g=nx.Graph()
    #filepath=r'D:\program\data\partialkanonmity\newmovies.txt'
    filepath=r'D:\program\data\partialkanonmity\polbooks.txt'
    #filepath=r'D:\program\data\partialkanonmity\citation-raw.txt'
    read_file_txt(g,path=filepath)
    tempname=os.path.split(filepath)
    outName=os.getcwd()+r'\data\p_'+tempname[1]
    f=open(outName,'w')
    for k in range(5,45,5):     
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



if __name__=="__main__": 
    print 'ss'
    test_subrisk()


   
