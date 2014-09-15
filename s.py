import networkx as nx
import matplotlib.pyplot as plt

def sh(g):
    nx.draw(g,with_labels = True)
    plt.show()
def chlist(x):
    for i,y in enumerate(x):
        if y%2==0:
            x.remove(y)

def madd(x,y):
    return x+y

def m(x):
    for i,y in enumerate(x):
        if y%2==0:
            x.remove(y)

        
        
