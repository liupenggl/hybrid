import exceptions
import networkx as nx
class dog(object):
    'test class'
    v=0
    def __init__(self,age,bark="wang"):
        dog.v+=1
        self.age=age
        self.bark=bark
        print("dog.=%d",dog.v)
    def show(self):
        print str(self.v)+":"+self.bark
    def ad(self):
        pd(self)
    @property
    def name(self):
        return self.bark

def pd(data):
    print data.age



def para(*p):
    print p


def parad(**p):
    print p
def ta(att_d=None,**attr):
    print att_d,'\n'
    print "attr:",attr

def itest():
    x=[(3,4),(2,3)]
    g=nx.Graph()
    g.add_path(range(4))
    y=(3,4)
    try:
        print y in g.node
        g.adj[y]={}
    except TypeError:
        print "type error"

if __name__=='__main__':
    #print " In main"
    #g=dog(3)
    #print hasattr(g,'showg')
    #g.ad()
    #print "property name ",g.name
    ta(att_d=7,d=5,y="YYY",t='time')
    #itest()
 
 