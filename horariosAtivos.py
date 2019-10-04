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
	ids =[]

	for x in myresult:
		tempArray = []
		matriculas.append(x[1])
		ids.append(x[0])
		for s in x[2]:
			tempArray.append(int(s))
		horarios.append(tempArray)
	dist = DistanceMetric.get_metric('hamming')
	#print("matriculas %s"%matriculas)
	m = dist.pairwise(horarios)

	return [m,matriculas,ids]


#Gerando matriz de dissimilaridade
#gruposFormadosMatr = []
#gruposFormados = []
def criaCLustersBySchedule(turma,nMembers):
    import clusterHierarquico as ch
    query = "select h.id_usuario,u.matricula,h.sequencia from horario_aluno h, usuario u, turma_aluno ta where h.ativo = 'S' and u.id = h.id_usuario and u.id = ta.id_aluno and ta.id_turma="+str(turma)+" and u.controle=0";
    resultado = genDistanceMatrix(query)
    print("matriz de similaridade %s"%resultado[0])
    print("matriculas %s"%resultado[1])
    matriculas = resultado[1]
    ids = resultado[2]
    #createDendogram(resultado[0])
    grupos = ch.criaGrupos(resultado[0], int(nMembers))
    #
    qryValues = ""
    qryGrupo = ""
    mycursor = conexao.mydb.cursor()
    #####
    j=1
    for g in grupos:
        qryGrupo = "insert into grupo (nome,id_turma) values('Grupo Temp "+str(j)+"',"+str(turma)+")";
        print("qryGrupo %s"%qryGrupo)
        mycursor.execute(qryGrupo)
        #pega o ultimo id de grupo cadastrado
        lastIdGrupo = mycursor.lastrowid
        print ("lastIdGrupo %s"%lastIdGrupo)
        #inicia o cadastro dos membros deste grupo
        qryValues = ""
        if(lastIdGrupo != ""):
            i=1
            for m in g:
                qryValues+= "("+str(lastIdGrupo)+",'" +str(ids[m])+ "')"
                if i < len(g):
                    qryValues=qryValues + "," 
                    i = i +1
                    j+=1
	#insere os membros do grupo atual
            print("qryValues %s"%qryValues)
            qryInsert = "insert into grupo_aluno (id_grupo,id_aluno) values "+qryValues
            print("qryInsert %s"%qryInsert)
            try:
                mycursor.execute(qryInsert)
            except:
                return -1
    conexao.mydb.commit()
    return mycursor.rowcount