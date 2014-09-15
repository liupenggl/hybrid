import networkx as nx
import matplotlib.pyplot as plt
from rsel import sh
import os 
def ch(x):
    for each in x:
        if each==4:
            x.remove(each)

i=0
def ch2(x):
    i=0
    while i<len(x)-1:
        j=i+1
        while j<len(x):
            if(x[i]==x[j]):
                x.pop(j)
                x.pop(i)
                i=i-1
                break
            else:
                j=j+1
        i=i+1
 
def readFile(g,path="graph.txt"):
    f=open(path,'r')     
    for eachLine in f:
        if eachLine.find('*Edges')==-1:
            continue
        else:
            break
    for eachLine in f:
        if len(eachLine)<2:
            continue
        li=eachLine.strip().split()
        u=int(li[0])
        v=int(li[1])
        g.add_edge(u,v)
 
        
                
def main():
    print 'main running!'
##    g=nx.read_adjlist("te.adj",nodetype=int)
##    x=g.degree().values()
##    print x
    g=nx.Graph()
    s=os.getcwd()
    print s
    
    readFile(g,r"D:\program\data\graph.txt")
    nx.clustering(g)
    sh(g)
    plt.show()

if __name__=='__main__':
    main()
