#!/usr/bin/env python3
import conexao
import json
from sklearn.cluster import KMeans
from sklearn.neighbors import DistanceMetric
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
import createGrupos

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

#usando	
gruposFormadosMatr = []
gruposFormados = []
resultado = genDistanceMatrix("select h.id_usuario,u.matricula,h.sequencia from horario_aluno h, usuario u where ativo = 'S' and u.id = h.id_usuario")
gruposFormados = createGrupos.geraGrupos2(resultado[0],3)
for grupo in gruposFormados:
	gf = []
	for pos in grupo:
		gf.append(resultado[1][pos])
	gruposFormadosMatr.append(gf)
print("gruposFormadosMatr %s"%gruposFormadosMatr)

	#minmax_kmeans.runKmeans(horarios,2,2,2,10)
	#horarios_alunos = np.array(horarios)
	#kmeans = KMeans(n_clusters=2, random_state=0).fit(m)
	#print(kmeans.labels_)
M = genDistanceMatrix("select h.id_usuario,u.matricula,h.sequencia from horario_aluno h, usuario u where u.id = h.id_usuario and h.ativo = 'S' and (u.matricula = '20182TIJG0584' or u.matricula= '20182TIJG0649' or u.matricula = '20182TIJG0487')")
print("M %s"%M[0])

