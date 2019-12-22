import networkx as nx   #used to create the graph
import numpy as np      #useful to be faster
import folium           #used for map visualization
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
    p=[h]+p #collection all the route
    route=[p[0]] #initializatin the route from the starting point
    for i in range(len(p)-1): #getting all the steps
        if p[i+1] in G and p[i] in G: #if a point is not in G that's not possible to connect all of them
            route+=dijkstra(G, p[i], p[i+1])[1:] #calling the algorithm
        else:
            s="Not possible"
            return s
    return route

#print(start(creategraph(),1,[451,1799]))





def visualization(init,route):
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
    folium.PolyLine(locations=nodes_coord_inv,color="orange", weight=5, opacity=10).add_to(m)

    #plotting(marker)
    for i in range(len(route)):
        if route[i] in init[1:-1]: 
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
