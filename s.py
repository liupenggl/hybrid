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
    '''
    >>> madd(2,3)
    5
    '''
    print 'in test',x+y
    return x+y

def mi(x,y):
    '''
    >>> mi(3,2)
    1
    '''
    return x-y

def m(x):
    for i,y in enumerate(x):
        if y%2==0:
            x.remove(y)


if __name__=='__main__':
    import doctest,s
    doctest.testmod(verbose='v')
    print "mode test s"

        
        
