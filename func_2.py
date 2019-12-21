#!/usr/bin/env python
# coding: utf-8

# In[21]:


# This function is very similiar to the func_1 so comment's are the same
# Python program for Kruskal's algorithm to find 
# Minimum Spanning Tree of a given connected,  
# undirected and weighted graph 
  
from collections import defaultdict 


'''
Kruskal's algorithm is a greedy algorithm that finds a minimum spanning tree for a weighted undirected garph.
The algorithm operates by adding the egdes one by one in the order of their increasing lengths, so as to form a tree. 
Egdes are rejected if it's addition to the tree, forms a cycle. 
This continues till we have V-1 egdes in the tree. (V stands for the number of vertices).

'''

  
#Class to represent a graph 
class Graph: 
  
    def __init__(self,vertices): 
        self.V= vertices                 # No. of vertices 
        self.graph = []                  # default dictionary to store graph 
          
   
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


# In[22]:


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


# In[23]:


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


# In[24]:


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


# In[25]:


def create_graph(node_arr, param_1, param_2, param_3) :
    g = Graph(len(node_arr)) 
    for item in node_arr:
        i1 = int(item[param_1])
        i2 = int(item[param_2])
        i3 = int(item[param_3])
        
        g.addEdge(i1, i2, i3) 
    return g


# In[26]:


def get_smatest_neighbours(vs, graph):
    mst = graph.KruskalMST()
    all_nearest_neighbours = []
    for node1,node2,w  in mst: 
        for v in vs :
            if v == node1:
                all_nearest_neighbours.append(node2)
            elif v == node2:
                all_nearest_neighbours.append(node1)
    return all_nearest_neighbours


# In[27]:


distance_graph = create_graph(node_distances, 'node1', 'node2', 'distance')


# In[28]:


time_graph = create_graph(node_time, 'node1', 'node2', 'time')


# In[29]:


get_smatest_neighbours([3, 4], time_graph)


# In[30]:


get_smatest_neighbours([3, 4], distance_graph)


# In[ ]:




