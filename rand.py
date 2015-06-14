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
        return g.edges()
 
#--------------------------------------------------------------#

def add_edge(g,m):
    compl=nx.complement(g)
    if len(compl.edges())>=m:
        aedge=random.sample(compl.edges(),m)
        return aedge
    else:
        print "not enough nodes to add m edges, please check m"
        return compl.edges()
#--------------------------------------------------------------#

def binomial_con_di(z,node,g,m):
    """删除m条边 X，然后添加m条边Y，z 是节点的度，node节点的标签，g图
    """

    n1=m if m<=len(g[node]) else len(g[node])#delete at most min(m,node degree) edges, because a node has only len(g[node]) edges
    p1=1.0*n1/len(g.edges())# n1 trails whit deleting probality p1, delelte at most n1 edges.
    
    n2=m if m<=(len(g.nodes())-1-len(g[node])) else (len(g.nodes())-1-len(g[node]))#leave enough node for edges adding
    p2=1.0*n2/( len(g.nodes())*(len(g.nodes())-1)/2-len(g.edges()) )
 
    di=len(g[node])
    sum=0.0
    t=0
    while t<=n1:
        if z-di+t>=0 and z-di+t<=n2:
            sum=sum+stats.binom.pmf(t,n1,p1)*stats.binom.pmf(z-di+t,n2,p2)#adding z-di edges
        t+=1
    return sum

def rand_risk_v(node,g,m):
    """
    return the probability of the node can be reidentfy by m pertubation
    """
    pr=binomial_con_di(len(g[node]),node,g,m)#the prob of the degree of node not change.
    #print node
    #print pr

    prr=1-pr
#    f=open("temp.txt",'w')
    
    for each in g.nodes():
#        f.write('{0:>2} {1} {2} {3}'.format(each,' : ',binomial_con_di(len(g[node]),each,g,m),'\n'))
        prr=prr+binomial_con_di(len(g[node]),each,g,m)
    return pr*(1.0/prr) 
#    f.close()

def rand_risk(g,m):
    """
    return the max probability of the all the nodes  reidentfied by m pertubation
    """
    max=0
    #f=open("temp.txt",'w')

    for each in g:
        temp=rand_risk_v(each,g,m)
        #print '{0:>2} {1} {2} {3}'.format(each,' : ',temp,'\n')
        #f.write('{0:>2} {1} {2} {3}'.format(each,' : ',temp,'\n'))
        if max<temp:
            max=temp
            maxnode=each
 
    #f.close()
    print max
    return max,maxnode

def test_rand_risk():
    g=nx.Graph()
    #filepath=r'\newmovies.txt'
  
    #filepath=r'\citation-raw.txt'
    filepath=r'\polbooks.txt'
    #filepath=r'\graph.txt'
    filepath=os.getcwd()+r'\data'+ filepath
    read_file_txt(g,path=filepath)

    tempname=os.path.split(filepath)
    outName=os.getcwd()+r'\data\result\randrisk_'+tempname[1]
    f=open(outName,'w')
    
    for k in range(5,45,5):     
        m=3
        p=1.0/k
        r,node=rand_risk(g,m)
        mMax=len(g.edges())
        if r<=p:
            f.write('k={0} m={1} r={2}\n'.format(k, m, r))
        else:
            while r>p:
                m=m+1   #need modify
                r=rand_risk_v(node,g,m)
                
                if m>mMax:
                    f.write('Cannot perturbate successfully! k={0} m={1} r={2}\n'.format(k, m, r))
                    break
                f.write('k={0} m={1} node={2} r={3}\n'.format(k, m,node, r))
            
   
    f.close()  

if __name__=="__main__": 
    print 'ss'
    #g=nx.Graph()
    #g.add_edges_from([['0','1'],['1','2']])
    #g.add_node('3')
    #g.add_edge('2','4')
    #g.add_edge('3','4')
    #max,v=rand_risk(g,1)
    #print v,max

    #sh(g)

    test_rand_risk()