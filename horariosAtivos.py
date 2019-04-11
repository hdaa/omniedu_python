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
	print("dn %s"%dn)
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


import clusterHierarquico as ch
#Gerando matriz de dissimilaridade
#gruposFormadosMatr = []
#gruposFormados = []
turma = 1
query = "select h.id_usuario,u.matricula,h.sequencia from horario_aluno h, usuario u, turma_aluno ta where h.ativo = 'S' and u.id = h.id_usuario and u.id = ta.id_aluno and ta.id_turma="+str(turma)
resultado = genDistanceMatrix(query)
print("matriz de similaridade %s"%resultado[0])
print("matriculas %s"%resultado[1])
matriculas = resultado[1]
#createDendogram(resultado[0])
grupos = ch.criaGrupos(resultado[0], 4)
clusterMatriculas = []
#
qryValues = ""
j=1
for g in grupos:
	gm = []
	i=1
	qryValues += "("+str(turma)+",'"
	for m in g:
		qryValues=qryValues +matriculas[m]
		if i < len(g):
			qryValues=qryValues + ","
		else:
			qryValues=qryValues + "')"
		i = i +1
	if j < len(grupos):
		qryValues+=","
	j+=1

	print("qryValues %s"%qryValues)

qryInsert = "insert into grupo_temp (id_turma, formacao) values "+qryValues
print(qryInsert)
mycursor = conexao.mydb.cursor()
mycursor.execute(qryInsert)
conexao.mydb.commit()
print(mycursor.rowcount, "record inserted.")
#print("cluster matriculas %s"%clusterMatriculas)