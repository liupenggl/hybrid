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


def test1():
    g=nx.Graph()
    filepath=r'D:\program\code\hybrid\data\graph.txt'
    read_file_txt(g,path=filepath)
    sh(g)

def say(worker):
    print 'I am worker %s' % worker
    def dec(fn):
        print 'staring..'
        fn(*argv,**kwgs)
        print 'end.'
    return dec

@say("main")
def main(n):
    for i in range(n):
        print i*2
def da(g):
    g.add_edges_from([(1,2),(1,3),(1,4),(2,3),(3,4),(4,5),(4,6),(5,6),(5,7),(5,8),(6,7),(6,8),(7,8),(7,9)])
    return g


if __name__=="__main__":
    print 'sss'
    print sys.argv

    main(3)
for i in range(9):
    c[:,i]= c[:,i]/ c[:,i].sum()
