#This function is very similiar to the func_3 so most of the comment's are the same
import networkx as nx   #used to create the graph
import numpy as np      #useful to be faster
from itertools import permutations as per #getting all the permutation possible
import folium           #used for map visualization

'''
The checki function takes the whole route that we have collected and check if it has all the points that we have choose
'''

def checki(route,p):
    for i in range(len(p)):
        if p[i] not in route:
            return False
    return True

'''
dist function, taking the file path and a temporary variable, so we open the file and split every line into a list
then if the list starts with an "a" we have a connection, so we add them into a list with (point1, point2, weight of the connection
The boolean variable T is used to understand if we want just the network distance, where the weight between two points is just 1
'''
def dist(s,T):
    l=[]
    with open(s) as file:
        for line in file:
            a=line.split()
            if a[0]=="a":
                if T:
                    l.append((int(a[1]),int(a[2]),int(a[3])))
                else:
                    l.append((int(a[1]),int(a[2]),1)) 
    return l

'''
Here we create the graph using networkx
'''
def creategraph():
    G=nx.Graph()
    s=input("Put 1 for Physical Distance\nPut 2 for Time Distance\nPut 3 for the Network Distance:\n")
    if s=="1":
        G.add_weighted_edges_from(dist("USA-road-d.CAL.gr",True))
    elif s=="2":
        G.add_weighted_edges_from(dist("USA-road-t.CAL.gr",True))
    elif s=="3":
        G.add_weighted_edges_from(dist("USA-road-d.CAL.gr",False))
    else:
        print("Please follow the rules")
        return creategraph()
    return G


'''
Finally my version of dijkstra, it of course has to take the graph, the starting point and also the point that we have to reach
'''
def dijkstra(G,h,p):
    seen=set() #seen set, useful to understand if we reach the point
    distance=np.full(len(G.nodes)+1, np.inf) #distance array, all set to infinite, it will remember the mindistance that connect a point to another one
    daddy=np.full(len(G.nodes)+1, -1)        #is a list that will remember the connection between two points so if point 5 has min distance to point 2, daddy[5]=2
    distance[h]=0 #the Head has distance 0
    minvalue=np.full(len(G.nodes)+1, np.inf) #is a list that will remeber the minimum distance between the head to a point in the graph, all sets to -1 at the start
    minvalue[h]=0 #the minvalue of the head is of course 0
    daddy[h]=h #the starting point
    point=h #a variable used to understand which point we are checking
    seen.add(point) #so it is already seen
    while p not in seen: #the loops stops when you arrive in your destination
        point=np.where(minvalue == min(minvalue))[0][0] #from the minvalue list we take the one that has the minvalue in the whole array, we will check that point
        for elem in G.adj[point]: #for every elem adjacent to that point we will see what it has connected
            if G[point][elem]['weight']+distance[point]<distance[elem]: #if the distance of the adjacent to the point that we are checking plus the distance of the point to the head is lower
                distance[elem]=G[point][elem]["weight"]+distance[point] #to the one that we already have, we got a new minvalue point to reach that point, so we update our check list
                daddy[elem]=point                                       #we remember that what the father of the checked element is the point
                minvalue[elem]=distance[elem]                           #and we collect his distance, because it has to be the lower one
            minvalue[point]=np.inf                                      #and we set the point minvalue to infinite so we will not check it anymore and we don't fall into a loop
            seen.add(point)                                             #and we add the point into the seen
            
            
    path=[] #here we start to collect the path once we have got from the Head to the Destination point
    x=p     #we create the starting point from the destination
    while x!=h: #while x is not the head
        path.append(x) ##we check the father of each point
        x=daddy[x]     #and we put it into the list of point reached
    path.append(h) #we add the last value, the starting point 
    return path[::-1] #and we return the reverse path
'''
The core of the algorithm, it will return us the best route, in input we take the graph created with creategraph, 
also we get the Head of the route H and every next steps into the list p
'''
def start(G,h,p):
    fin=[h]+[p[len(p)-1]] #a list with the Head and the Destination element
    p=p[0:len(p)-1] #every point that we want to reach
    L_p=[] #L_p will be a temporary List that we will discuss later
    best=[] #the best path that we have found in term of elements inside it
    lenbest=float("inf") #his len that will starts from infinite
    m=1 #a variable that we will need to define the size of each permutation
    route=dijkstra(G, fin[0], fin[1])[1:] #checking if we have reach everypoint already just going from the Head to the Destination
    if checki(route,[fin[0]]+p+[fin[1]]): #so if checki returns True, we reached every point
            if len(route)<lenbest: #and if we get them in less steps, we have a new best route
                best=route
                lenbest=len(best)
    while True: #infinite loop
        route=[fin[0]] #all the routes starts with the starting point no?
        L_p=list(per(p,m)) #L_p will collect a list of every permutation of the points between the starts and the destination, with the size of m
        for i in range(len(L_p)): #for every permutation
            L_p[i]=[fin[0]]+list(L_p[i])+[fin[1]] #the single permutation will become a list with starting point plus steps plus destination
            for j in range(len(L_p[i])-1): #for every element inside it
                if L_p[i][j+1] in G and L_p[i][j] in G: #if the point is not in the graph that route is not possible
                    route+=dijkstra(G, L_p[i][j], L_p[i][j+1])[1:] #here we call the algorithm
                else:
                    continue
            if checki(route,[fin[0]]+p+[fin[1]]): #again checki if our new route is good enough
                if len(route)<lenbest:
                    best=route
                    lenbest=len(best)   
            route=[fin[0]] #here we restart the route
        m+=1 #if every permutation with a size is already checked we go to the next one in order of the size
        if m>len(p): #if the size is > than the list of point that we have to check we already have a best one
            return best #so we will return our route


def visualization(start,route):
    lines = open("USA-road-d.CAL.co", "r").read().splitlines() #importing coordinates
    node = []
    for i in lines:    
        node.append(i.split())
    x=[[el[1],(int(el[2])*10**-6,int(el[3])*10**-6)] for el in node if el[0]=='v'] #extracting node and coordinates(calculated)
    y=[el[1] for el in x]  #coordinates    
    coord={} #bulding dict {node: coordinate(x,y)}
    for i in range(len(x)):
        coord[i+1] = y[i]    
    nodes_coord = [coord[i] for i in route]
    nodes_coord_inv = [(b,a) for a,b in nodes_coord]

    #visualization part
    #creating a Folium map object centered on the starting point
    m=folium.Map(nodes_coord_inv[0],zoom_start=15)
    
    # plotting edge(routes between nodes)
    folium.PolyLine(locations=nodes_coord_inv,color="yellow", weight=5, opacity=10).add_to(m)

    #plotting(marker)
    for i in range(len(route)):
        if route[i] in start[1:-1]: 
            folium.Marker(location=nodes_coord_inv[i], popup=route[i], icon=folium.Icon(icon='glyphicon glyphicon-arrow-down')).add_to(m)
        elif i == 0:
            folium.Marker(location=nodes_coord_inv[i], popup=route[i], icon=folium.Icon(icon='glyphicon glyphicon-play')).add_to(m)
        elif i == len(route)-1:
            folium.Marker(location=nodes_coord_inv[i], popup=route[i], icon=folium.Icon(icon='glyphicon glyphicon-flag')).add_to(m)
        else:
            folium.CircleMarker(location=nodes_coord_inv[i], popup=route[i], color= 'red', number_of_sides=0 ,radius=3).add_to(m)

    #selectable layers
    folium.TileLayer('openstreetmap').add_to(m)
    folium.TileLayer('cartodbdark_matter').add_to(m)
    folium.TileLayer('stamenwatercolor').add_to(m)
    folium.TileLayer('stamentoner').add_to(m)
    folium.LayerControl().add_to(m)
    return m


#print(start(creategraph(),1,[451,1050017,1799]))

