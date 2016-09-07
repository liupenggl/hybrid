#-*- coding:utf-8 -*-
from scipy import stats
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from gfile import *
import networkx as nx
import random
import string 
import sys
from prandom import *
from rsel import *
from community_louvain import *

def test1():
    g=nx.Graph()
    filepath=r'D:\program\code\hybrid\data\graph.txt'
    read_file_txt(g,path=filepath)
    sh(g)

def da(g):
    g.add_edges_from([(1,2),(1,3),(1,4),(2,3),(3,4),(4,5),(4,6),(5,6),(5,7),(5,8),(6,7),(6,8),(7,8),(7,9)])
    return g

def shFast(result,G):
    size = float(len(set(result.values())))
    pos = nx.spring_layout(G)
    count = 0.
    for com in set(result.values()):
        count = count + 1.
        list_nodes = [nodes for nodes in result.keys() if result[nodes] == com]
        nx.draw_networkx_nodes(G, pos, list_nodes, node_size=20, node_color=str(count / size))
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.show()

if __name__=="__main__":
    print 'sss'
    g = nx.Graph()
    da(g)
    r = best_partition(g)
    shFast(r, g)


