import networkx as nx
import matplotlib.pyplot as plt
from rsel import sh
import os 

def f(a,L=[]):
    L.append(a)
    return L



def main():
    print 'main running! In temp.py'
 
    s=os.getcwd()
    print s
    x=3
    if x>5:
       print "great 5"
    elif x<2:
        print "less than 2"
    else:
        print "between"

    print f(1)
    print f(2)




 

if __name__=='__main__':
    main()