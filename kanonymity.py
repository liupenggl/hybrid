import os
import networkx as nx
import matplotlib.pyplot as plt


def readfile_net(g,path=None):
 
    #path="D:\\program\\code\\hybrid\\data\\graph.txt"
    g.clear()
    import shlex
    try:
        f=open(path,'r')
    except :
        print "readfile_net error" 

    #for line in f:
    #    if line.strip().lower().startswith("*vertices"):
    #        break
    for line in f:
        if line.lower().startswith("*edges"):
            break

        #temp=shlex.split(line)
        #if len(temp)>=2:
        #    v,l=temp[0:2]
        #    g.add_node(v,label=l) #For simplity,we do not use the node's attribute

    for line in f:
        temp=line.split()
        if len(temp)<2:
            continue
        u,v=temp[0:2]
        g.add_edge(u,v)
   
    f.close()
    return g

def sh(g):
    nx.draw(g,with_labels = True,pos=nx.spring_layout(g))
    plt.show()

def graphtodegree(g):
    deglist=list() #deglist is a list of dictionary [{'name': ,'deg': , 'diff':},...]
    for k,v in nx.degree(g).items():
        #print k,v
        deglist.append({'name':k,'deg':v,'diff':None})

    return deglist

def degree_diff(deglist,begin,end):
    value=0
    end=end-1
    while begin<end:
        value=value+deglist[begin]['deg']-deglist[end]['deg']
        end-=1
    return value

def degreee_anony(deglist,k): #greed algorithm use max differece
  
    begin=0  #deglist is a list of dictionary [{'name':"the node" ,'deg':"the node's degreee , 'diff': },...]
    nodep=0
    end=len(deglist)

    while(end-nodep>=2*k):
        i=0
        temp=0
        flag=0

        temp=deglist[nodep]['deg']-deglist[nodep+1]['deg']
        while i<2*k-1:
            x=deglist[nodep+i]['deg']-deglist[nodep+i+1]['deg']
            if x>temp:
                temp=x
                flag=i
            i+=1
        if end-nodep-flag-1<k:
            flag=flag-(k-(end-nodep-flag-1))
        if flag<k-1:
            flag=k-1
        deglist[nodep+flag+1]['flaga']=1
        nodep=nodep+1+flag;

 
    j=0 #Calculate the 'diff' and 'flaga'
    temp=deglist[0]['deg']
    for each in deglist:
        if len(each)==4:
            j+=1;
            temp=each['deg']
        each['flaga']=j
        each['diff']=temp-each['deg']
    rvalue=0
    for each in deglist:
        rvalue=rvalue+each['diff']
    return rvalue

def diffSelect(deglist):
    temp=[]
    for each in deglist:
        if each['diff']!=0:
            temp.append(each)
    deglist=temp
    return deglist


def addEdge(g,deglist):
    i=0
    while i<len(deglist)-1:
        flag=0
        j=i+1
        while j<len(deglist):
            if deglist[i]['name'] not in g.edge[deglist[j]['name']]:
                g.add_edge(deglist[i]['name'],deglist[j]['name'])
                deglist[i]['diff']=deglist[i]['diff']-1
                deglist[j]['diff']=deglist[j]['diff']-1
                
                if deglist[j]['diff']==0:
                    deglist.pop(j)
                if deglist[i]['diff']==0:
                    deglist.pop(i)
                flag=1
                break
            j=j+1
        if flag!=1:
            i=i+1
    if len(deglist)==0:
        return 0
    else:
        return 1

def addNode(g,deglist):
    for each in deglist:
        while each['diff']>0:
            g.add_edge(each['name'],'a'+str(each['diff']))
            each['diff']-=1


    



             


#def graphtolist(g):
#    degree=[]
#    for x in g:


if __name__=='__main__':
    print 'sss'
    #filepath=os.getcwd()
    #filepath=os.path.join(filepath,"data\\AFFIL.NET")

    g=nx.Graph()
    #readfile_net(g,path=filepath)
    readfile_net(g)

    deglist=graphtodegree(g)
 
    deglist.sort(key=lambda deg:deg['deg'],reverse=True)

    degreee_anony(deglist,9)

    deglist=diffSelect(deglist)

    addEdge(g,deglist)

    addNode(g,deglist)
    sh(g)
