def retornaMenor(distance_matrix):
	import numpy as np
	for i in range(0,len(distance_matrix)):
		for j in range(0,len(distance_matrix[0])):
			if(i==j):
				distance_matrix[i][j]=100
	minimoCL=[]
	for i in range(0,len(distance_matrix)):
		minimoCL.append(np.where(distance_matrix[i,:] == min(distance_matrix[i,:]))[0][0])
	#print("npwhere %s"%np.where(distance_matrix == distance_matrix.min())
	print("minimoCL %s"%minimoCL)
	menor = 100
	menorCol = 0
	menorLinha = 0
	h = 0
	for m in minimoCL:
		if distance_matrix[h,m] < menor:
			menor = distance_matrix[h,m]
			menorLinha = h
			menorCol = m
		h=h+1
	return [menor,menorLinha,menorCol]

def countElements(lista):
	conta = 0
	for i in range(0,len(lista)):
		conta = conta + len(lista[i])
	return conta

def criaGrupos(distance_matrix, nMembers):
	from math import ceil
	import numpy as np
	countMembers = 0
	clusters =[]
	totalClusters = ceil(len(distance_matrix)/nMembers)
	nClusters = 0
	menorDist = 100
	menorDistCol = 0
	grupo = []
	t1 = 0
	t2 = 0

	for i in range(0, len(distance_matrix)):
		for j in range(i, len(distance_matrix)):
			distance_matrix[i][j] = 100

	#print("distance_matrix %s"%distance_matrix)
	
	while len(clusters) < totalClusters:
		#Iniciando novo cluster
		grupo = []
		resultadoMenor = retornaMenor(distance_matrix)
		grupo.append(resultadoMenor[1])
		grupo.append(resultadoMenor[2])
		distance_matrix[resultadoMenor[1]][resultadoMenor[2]] = 100
		totalMembros = 0
		
		if len(grupo) == nMembers or (len(grupo) + countElements(clusters)) == len(distance_matrix):
			distance_matrix[resultadoMenor[1],:] = 100
			distance_matrix[:,resultadoMenor[1]] = 100
			distance_matrix[:,resultadoMenor[2]] = 100
			distance_matrix[resultadoMenor[2],:] = 100
		else:

			t1 = resultadoMenor[1]
			t2 = resultadoMenor[2]
			#print("distance_matrix inicio cluster %s"%distance_matrix)
			while (len(grupo) < nMembers) and (len(grupo) + countElements(clusters)) < len(distance_matrix):
				#se o grupo tiver menos membros que o esperado continuar procurando os mais próximos
				#verifica se do par linha,coluna qual a distancia minima entre linha e os outros membros e entre
				# coluna e os outros membros
				print("t1 %s"%t1)
				print("t2 %s"%t2)

				#verifica termo 1
				xx = np.where(np.logical_or(min(distance_matrix[t1,:]) == distance_matrix[t1,:], min(distance_matrix[:,t1]) == distance_matrix[:,t1]))
				print("xx %s"%xx)
				print("xx [0] %s"%xx[0][0])
				print("xx 1 %s"%xx[0][1])
				print("dm1 xx[0][0] %s"%distance_matrix[t1][xx[0][0]])
				print("dm1 xx[0][1] %s"%distance_matrix[xx[0][1]][t1])

				if(distance_matrix[t1][xx[0][0]] < distance_matrix[xx[0][1]][t1]):
					tt1 = [t1,xx[0][0]]
				else:
					tt1= [xx[0][1],t1]

				print("tt1 %s "%tt1)

				#termo 2
				yy = np.where(np.logical_or(min(distance_matrix[t2,:]) == distance_matrix[t2,:], min(distance_matrix[:,t2]) == distance_matrix[:,t2]))
				print("yy %s"%yy)
				print("yy [0] %s"%yy[0][0])
				print("yy [1] %s"%yy[0][1])
				print("dm2 yy[0][0] %s"%distance_matrix[t2][yy[0][0]])
				print("dm2 yy[0][1] %s"%distance_matrix[yy[0][1]][t2])
				if(distance_matrix[t2][yy[0][0]] < distance_matrix[yy[0][1]][t2]):
					tt2 = [t2,yy[0][0]]
				else:
					tt2= [yy[0][1],t2]

				print("tt2 %s "%tt2)
				print("dM tt1 %s"%distance_matrix[tt1[0]][tt1[1]])
				print("dM tt2 %s"%distance_matrix[tt2[0]][tt2[1]])

				#verfica se t1 ou t2 estah mais proximo de qualquer outro ponto
				if(distance_matrix[tt1[0]][tt1[1]] < distance_matrix[tt2[0]][tt2[1]]):
					#se t1 tiver o termo mais proximos o valor de distance_matrix[tt1[0]][tt1[1]] recebera 100
					# e todos os valores da linha t2 e da coluna t2 receberao 100
					distance_matrix[tt1[0]][tt1[1]] = 100
					distance_matrix[t2,:]=100
					distance_matrix[:,t2]=100
					v = np.where(np.isin(tt1, grupo, invert=True))
					print("v %s"%v)
					print("v[0][0] %s"%tt1[v[0][0]])
					grupo.append(tt1[v[0][0]])
					t1 = tt1[0]
					t2 = tt1[1]
					#se a quantidade de membros do grupo for igual ao desejado as colunas e linhas t1 tb sao setadas para 100
					if(len(grupo) == nMembers):
						distance_matrix[t1,:]=100
						distance_matrix[:,t1]=100
						distance_matrix[:,tt1[v[0][0]]]=100
						distance_matrix[tt1[v[0][0]],:]=100
						
				else:
					#se t2 tiver o termo mais proximos o valor de distance_matrix[tt2[0]][tt2[1]] recebera 100
					# e todos os valores da linha t1 e da coluna t1 receberao 100
					distance_matrix[tt2[0]][tt2[1]] = 100
					distance_matrix[t1,:]=100
					distance_matrix[:,t1]=100
					print("np is in %s"%np.isin(tt2, grupo, invert=True))
					v = np.where(np.isin(tt2, grupo, invert=True))
					print("v %s"%v)
					print("v[0][0] %s"%tt2[v[0][0]])
					grupo.append(tt2[v[0][0]])
					t1 = tt2[0]
					t2 = tt2[1]
					#se a quantidade de membros do grupo for igual ao desejado as colunas e linhas t2 tb sao setadas para 100
					if(len(grupo) == nMembers):
						distance_matrix[t2,:]=100
						distance_matrix[:,t2]=100
						distance_matrix[:,tt2[v[0][0]]]=100
						distance_matrix[tt2[v[0][0]],:]=100
				print("grupo %s"%grupo)
			#####
		clusters.append(grupo)
		print("clusters %s"%clusters)
	#clusters finais
	print("clusters finais %s"%clusters)
	return clusters





