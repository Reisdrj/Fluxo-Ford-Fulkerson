import networkx as nx
import matplotlib
from copy import deepcopy

import matplotlib.pyplot as plt

def verificar(edges, node):
  soma = 0
  for i in range(len(edges)):
    if edges[i][1] == node:
      soma += edges[i][2]
  if(soma == 0):
    return 1
  else:
    return 0

def reduceFlow(path, edges, reverseEdges, cutFlow):
  print(path)
  for i in range(len(path)):
    for j in range(len(edges)):
      if edges[j][0] == path[i] and edges[j][1] == path[i+1] and edges[j][2] != 0:
        edges[j][2] -= cutFlow
  return

def findWeight(node1, node2, edges):
  for i in range(len(edges)):
    if edges[i][0] == node1 and edges[i][1] == node2:
        return edges[i][2]

def copyEdges(originalEdges):
  inverseEdges = deepcopy(d)
  for i in range(len(d)):
    inverseEdges[i][2] = 0
    originalEdges[i][2] = int(originalEdges[i][2])
  return inverseEdges

def sucessors(node, edges):
  sucessors = []
  for i in range(len(edges)):
    if edges[i][0] == node and edges[i][2] != 0:
      sucessors.append(edges[i][1])

  return sucessors

def keepPath(path, finalPath, edges):
    auxPath = deepcopy(path)
    lastNode = auxPath[len(auxPath)-1]
    suc = sucessors(lastNode, edges)
    if(len(suc) > 1):
        for i in range(len(suc)):
            if suc[i] == 'T':
              auxPath.append(suc[i])
              finalPath.append(auxPath)
              return
            newPath = deepcopy(auxPath)
            newPath.append(suc[i])
            keepPath(newPath, finalPath,edges)
    else:
        if(suc[0] == 'T'):
            auxPath.append(suc[0])
            finalPath.append(auxPath)
            return
        newPath = deepcopy(auxPath)
        newPath.append(suc[0])
        keepPath(newPath, finalPath, edges)


#Creating Graph
G = nx.read_weighted_edgelist('entrada.txt', nodetype=str, create_using = nx.DiGraph())
existPath = 0
paths = []
f = open("entrada.txt", "r")
d = [(line.strip()).split() for line in f.readlines()]
f.close()
nodes = list(G.nodes)

#Getting all the path from the graph
keepPath(list(d[0][0]), paths, d)
di = copyEdges(d)
print(paths)
#Ford-Fulkerson
while existPath != -1:
    existPath = 0
    flow = 0
    minimum = 0
    weights = []
    for i in range(len(paths)):
      #print(paths[i])
      weights = []
      for j in range(len(paths[i])-1):
          weights.append(findWeight(paths[i][j], paths[i][j+1], d))
      minimum = min(weights)
      print(d)
      print(minimum)
      if(minimum > 0):
        flow += minimum
        reduceFlow(paths[i], d, di, minimum)
      else:
        continue
    vef = verificar(d, 'G')
    if(vef):
       break
    existPath = -1

print(flow)
#Plotting Graph
pos = nx.spring_layout(G)
edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
nx.draw(G, pos, with_labels=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
plt.savefig("GrafoTeste.png")
