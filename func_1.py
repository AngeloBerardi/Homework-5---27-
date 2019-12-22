#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Python program for Kruskal's algorithm to find 
# Minimum Spanning Tree of a given connected,  
# undirected and weighted graph 
  
from collections import defaultdict
import folium           #used for map visualization
import networkx as nx	#used for map visualization
import io

'''
Kruskal's algorithm is a greedy algorithm that finds a minimum spanning tree for a weighted undirected garph.
The algorithm operates by adding the egdes one by one in the order of their increasing lengths, so as to form a tree. 
Egdes are rejected if it's addition to the tree, forms a cycle. 
This continues till we have V-1 egdes in the tree. (V stands for the number of vertices).
'''
    
    
    
#Class to represent a graph 
class Graph: 
  
    def __init__(self,vertices): 
        self.V= vertices #No. of vertices 
        self.graph = [] # default dictionary to store graph 
          
   
    # function to add an edge to graph 
    def addEdge(self,u,v,w): 
        self.graph.append([u,v,w]) 
  
    # A utility function to find set of an element i 
    # (uses path compression technique) 
    def find(self, parent, i): 
        if parent[i] == i: 
            return i 
        return self.find(parent, parent[i]) 
  
    # A function that does union of two sets of x and y 
    # (uses union by rank) 
    def union(self, parent, rank, x, y): 
        xroot = self.find(parent, x) 
        yroot = self.find(parent, y) 
  
        # Attach smaller rank tree under root of  
        # high rank tree (Union by Rank) 
        if rank[xroot] < rank[yroot]: 
            parent[xroot] = yroot 
        elif rank[xroot] > rank[yroot]: 
            parent[yroot] = xroot 
  
        # If ranks are same, then make one as root  
        # and increment its rank by one 
        else : 
            parent[yroot] = xroot 
            rank[xroot] += 1
  
    # The main function to construct MST using Kruskal's  
        # algorithm 
    def KruskalMST(self): 
  
        result =[] #This will store the resultant MST 
  
        i = 0 # An index variable, used for sorted edges 
        e = 0 # An index variable, used for result[] 
  
            # Step 1:  Sort all the edges in non-decreasing  
                # order of their 
                # weight.  If we are not allowed to change the  
                # given graph, we can create a copy of graph 
        self.graph =  sorted(self.graph,key=lambda item: item[2]) 
  
        parent = [] ; rank = [] 
  
        # Create V subsets with single elements 
        for node in range(self.V): 
            parent.append(node) 
            rank.append(0) 
      
        # Number of edges to be taken is equal to V-1 
        while e < self.V -1 and i < len(self.graph) : 
  
            # Step 2: Pick the smallest edge and increment  
                    # the index for next iteration 
            u,v,w =  self.graph[i] 
            i = i + 1
            x = self.find(parent, u) 
            y = self.find(parent ,v) 
  
            # If including this edge does't cause cycle,  
                        # include it in result and increment the index 
                        # of result for next edge 
            if x != y: 
                e = e + 1     
                result.append([u,v,w]) 
                self.union(parent, rank, x, y)             
        return result
    


# In[2]:


#load datas

#distance
with open('USA-road-d.CAL.gr', 'r') as f:
    data = f.read().split('\n')
    
data = data[8:]
data = [ele for ele in data if ele]
node_distances = []
for item in data:
    node_distances.append({
        "node1": item.split(' ')[1],
                "node2": item.split(' ')[2], 
                "distance": int(item.split(' ')[3]), 
    })


# In[3]:


#time
with open('USA-road-t.CAL.gr', 'r') as f:
    data = f.read().split('\n')
    
data = data[8:]
data = [ele for ele in data if ele]
node_time = []
for item in data:
    node_time.append({
        "node1": item.split(' ')[1],
                "node2": item.split(' ')[2], 
                "time": item.split(' ')[3], 
    })


# In[4]:


#coordinates
with open('USA-road-d.CAL.co', 'r') as f:
    data = f.read().split('\n')
    
data = data[8:]
data = [ele for ele in data if ele]
node_coords = []
for item in data:
    node_coords.append({
        "node": item.split(' ')[1],
                "lat": item.split(' ')[2], 
                "lng": item.split(' ')[3], 
    })


# In[5]:


def create_graph(node_arr, param_1, param_2, param_3) :
    g = Graph(len(node_arr)) 
    for item in node_arr:
        i1 = int(item[param_1])
        i2 = int(item[param_2])
        i3 = int(item[param_3])
        
        g.addEdge(i1, i2, i3) 
    return g


# In[6]:


def get_neighbours(v, graph, d):
    mst = graph.KruskalMST()
    all_nearest_neighbours = []
    for node1,node2,w  in mst: 
        if w <= d :
            if v == node1:
                all_nearest_neighbours.append(node2)
            elif v == node2:
                all_nearest_neighbours.append(node1)
#         if w <= d and (v == node1 or v == node2):
#             all_nearest_neighbours.append([node1,node2,w])    
    return all_nearest_neighbours


# In[7]:


distance_graph = create_graph(node_distances, 'node1', 'node2', 'distance')


# In[8]:


time_graph = create_graph(node_time, 'node1', 'node2', 'time')


# In[9]:


get_neighbours(2, distance_graph, 2389)


# In[10]:


get_neighbours(2, time_graph, 2389)


# In[ ]:


def visualization(node_in,nodes_out,weight):

    #extracting coordinates
    lines = open("USA-road-d.CAL.co", "r").read().splitlines()
    node = []
    for i in lines:    
        node.append(i.split())
    x=[[el[1],(int(el[2])*10**-6,int(el[3])*10**-6)] for el in node if el[0]=='v'] #extracting node and coordinates
    y=[el[1] for el in x]  #coordinates
    y=[(a,b) for b,a in y]

    #bulding dict {node: coordinate(x,y)}
    coord={}
    for i in range(len(x)):
        coord[i+1] = y[i]

    #extracting edges
    lines = open("USA-road-d.CAL.gr", "r").read().splitlines()
    edges = []
    for i in lines:    
        edges.append(i.split())
    d_edges=[(int(el[1]),int(el[2])) for el in edges if el[0]=='a']

    #build the nx graph
    G=nx.Graph()   
    G.add_nodes_from([int(el[1]) for el in node if el[0]=='v'])
    G.add_edges_from(d_edges)
    
    #building coordinates for plotting the routes
    appo =[]
    for i in [node_in]+nodes_out:
        for j in list(G.edges(i)):
            if j[1] in [node_in]+nodes_out:
                appo.append(j)
    coord_edges = [(coord[i],coord[j]) for i,j in appo]
    
    #building coordinates for plotting nodes
    in_coord = coord[node_in]
    out_coord =[]
    for i in nodes_out:
        out_coord.append(coord[i])
        
    m=folium.Map(in_coord,zoom_start=16)

    #plot nearest nodes marker 
    for i in range(len(out_coord)):
        folium.Marker(location=out_coord[i], popup=nodes_out[i],radius=2, icon=folium.Icon(icon='glyphicon glyphicon-ok-sign',color='red')).add_to(m)

    #plot input node marker
    folium.Marker(location=in_coord, popup=node_in,radius=2, icon=folium.Icon(icon='glyphicon glyphicon-arrow-down',color='green')).add_to(m)

    #plot route
    if weight == 1:
        color = 'blue'
    elif weight == 2:
        color = 'yellow'
    else:
        color= 'green'
    folium.PolyLine(locations=coord_edges,color=color, weight=5, opacity=10).add_to(m)    

    #selectable layers
    folium.TileLayer('openstreetmap').add_to(m)
    folium.TileLayer('cartodbdark_matter').add_to(m)
    folium.TileLayer('stamenwatercolor').add_to(m)
    folium.TileLayer('stamentoner').add_to(m)
    folium.LayerControl().add_to(m)
    
    return m
