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

def m(mm):
 
    def inm():
        print"in inm()"
    def inx():
        print "in inx"
    return inx

def entryExit(f):
    def new_f():
        print "Entering",f.__name__
        f()
        print "Exite",f.__name__
    return new_f
@entryExit
def func1():
    print "inside  func1()"
@m
def func2():
    print "inside  func2()"

def spamrun(fn):
    def sayspam(*args):
        print "in sayspam"
        fn(2,6)
    return sayspam
@spamrun
def useful(a,b):
    print a**2,b**2


 

def fnn(*args):
    print "in fnn"
    f=useful
    return f(*args)

if __name__=='__main__':
    fnn(3,4)
 
  