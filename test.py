import time

import networkx as nx

from database.DAO import DAO
from model.model import Model

"""for i in DAO.getAllAirports():
    print(i)"""

myModel = Model()
myModel.build_graph(5)
myModel.printGraphDetails()

v0 = myModel.getAllNodes()[0]

connessa = list(nx.node_connected_component(myModel._grafo, v0))
v1 = connessa[10]

pathD = myModel.trovaCamminoD(v0, v1)
pathBFS = myModel.trovaCamminoBFS(v0, v1)
pathDFS = myModel.trovaCamminoDFS(v0, v1)

print("Metodo di Dijkstra")
print(*pathD, sep=" \n")
print("-------")
print("Metodo di Breadth First")
print(*pathBFS, sep=" \n")
print("-------")
print("Metodo di Depth First")
print(*pathDFS, sep=" \n")
print("-------")

t0 = time.time()
bestPath, bestScore = myModel.getCamminoOttimo(v0, v1, 3)
t1 = time.time()
print(f"Cammino ottimo ha peso {bestScore}, trovato in {t1 - t0} secondi")
print(*bestPath, sep="\n")
