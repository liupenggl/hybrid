import exceptions
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

if __name__=='__main__':
    #print " In main"
    #g=dog(3)
    #print hasattr(g,'showg')
    #g.ad()
    #print "property name ",g.name
 