#!/usr/bin/env python3
import conexao
import json
from sklearn.cluster import KMeans
from sklearn.neighbors import DistanceMetric
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

from matplotlib import pyplot as plt
import createGrupos

def createGraph(matrix):
	import networkx as nx
	G = nx.from_numpy_matrix(matrix)
	edge_labels = dict(((u, v), d["weight"]) for u, v, d in G.edges(data=True) if d["weight"] > 0.5)
	pos = nx.spring_layout(G)
	nx.draw(G, pos)
	nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
	nx.draw(G,pos,node_size=500, with_labels=True)
	plt.show()
	


def createDendogram(matrix):
	from sklearn.cluster import AgglomerativeClustering
	cluster = AgglomerativeClustering(n_clusters=6, affinity='euclidean', linkage='ward')  
	cx = cluster.fit_predict(matrix)  
	print(cx)
	Z = linkage(matrix, 'single')
	#print("Z %s"%Z)
	fig = plt.figure(figsize=(25, 10))
	dn = dendrogram(Z)
	fl = fcluster(Z,6,criterion='maxclust')
	#print("dn %s"%dn)
	plt.show()


def findMaxWeightMatch(matrix):
	import networkx as nx
	G = nx.from_numpy_matrix(matrix)
	xx = nx.max_weight_matching(G)
	return xx

def genDistanceMatrix(query):
	mycursor = conexao.mydb.cursor()
	mycursor.execute(query)
	myresult = mycursor.fetchall()
	horarios =[]
	matriculas = []

	for x in myresult:
		tempArray = []
		matriculas.append(x[1])
		for s in x[2]:
			tempArray.append(int(s))
		horarios.append(tempArray)
	dist = DistanceMetric.get_metric('hamming')
	#print("matriculas %s"%matriculas)
	m = dist.pairwise(horarios)

	return [m,matriculas]



#Gerando matriz de dissimilaridade
#gruposFormadosMatr = []
#gruposFormados = []
resultado = genDistanceMatrix("select h.id_usuario,u.matricula,h.sequencia from horario_aluno h, usuario u where ativo = 'S' and u.id = h.id_usuario")
print("matriz de similaridade %s"%resultado[0])
import shrinkingCluster as sc
resCluster =sc.SuperCluster(resultado[0], 4,3, 2,1,1)
print(resCluster)

#print(resultado[0])
#ds = 1-2*resultado[0]
#print(ds)
#np.fill_diagonal(ds,0)
#print(ds)
#createDendogram(1-resultado[0])
#metodos de criacao de grupos
#gruposFormados = createGrupos.geraGrupos2(1-resultado[0],3)
#for grupo in gruposFormados:
	#gf = []
	#for pos in grupo:
#		gf.append(resultado[1][pos])
#	gruposFormadosMatr.append(gf)

#print(gruposFormadosMatr)

#createGraph(1-resultado[0])

#print(findMaxWeightMatch(1-resultado[0]))

#createGrupos.geraGruposG(1-resultado[0], 3)


#print(xx)
#print("G edges %s"%G.edges(data=True))

#print(edge_labels)
#edge_colors = dict(((u, v), 'b') for u, v, d in G.edges(data=True) if d["weight"] > 0.5)
#edge_colors = dict(((u, v), 'red') for u, v, d in G.edges(data=True) if d["weight"] >= 0.5) 
#edge_colors.update(dict(((u, v), '#F08080') for u, v, d in G.edges(data=True) if d["weight"] < 0.5))
#print(edge_colors)



	#minmax_kmeans.runKmeans(horarios,2,2,2,10)
	#horarios_alunos = np.array(horarios)
	#kmeans = KMeans(n_clusters=2, random_state=0).fit(m)
	#print(kmeans.labels_)
#M = genDistanceMatrix("select h.id_usuario,u.matricula,h.sequencia from horario_aluno h, usuario u where u.id = h.id_usuario and h.ativo = 'S' and (u.matricula = '20182TIJG0584' or u.matricula= '20182TIJG0649' or u.matricula = '20182TIJG0487')")
#print("M %s"%M[0])

