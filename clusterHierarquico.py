def configMatrix(distance_matrix):
	for i in range(0, len(distance_matrix)):
		for j in range(i, len(distance_matrix)):
			distance_matrix[i][j] = 100
	#for i in range(0,len(distance_matrix)):
	#	for j in range(0,len(distance_matrix[0])):
	#		if(i==j):
	#			distance_matrix[i][j]=100
	return distance_matrix

def configMatrixByNiveis(distance_matrix,totalClusters):
	for i in range(0,totalClusters):
		for j in range(0,totalClusters):
			distance_matrix[i][j]=100
	return distance_matrix

def retornaMenor(distance_matrix):
	import numpy as np

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

def sobrou(jaTemGrupo,distance_matrix):
	import numpy as np
	f = range(0,len(distance_matrix))
	v = np.where(np.isin(f, jaTemGrupo, invert=True))
	print("sobrou: v %s"%v)
	return v

def criaGrupos(distance_matrix, nMembers):
    from math import ceil
    import numpy as np
    countMembers = 0
    clusters =[]
    totalClusters = ceil(len(distance_matrix)/nMembers)
    print("totalClusters %s"%totalClusters)
    nClusters = 0
    menorDist = 100
    menorDistCol = 0
    grupo = []
    distance_matrix = configMatrix(distance_matrix)
    print("distance_matrix")
    print(distance_matrix)
    #distance_matrix = configMatrixByNiveis(distance_matrix,totalClusters)
    #print("distance_matrix by niveis")
    #print(distance_matrix)
    jaTemGrupo = []
    t1 = 0
    t2 = 0

    while len(clusters) < totalClusters:
		#Iniciando novo clusterprint("totalClusters %s"%totalClusters)
        grupo = []
        print("primeira distance_matrix")
        print(distance_matrix)
        if (len(distance_matrix) - countElements(clusters)) <= nMembers:
            grupo = sobrou(jaTemGrupo,distance_matrix)[0]
            clusters.append(grupo)
            print("clusters %s"%clusters)
        else:
            resultadoMenor = retornaMenor(distance_matrix)
            grupo.append(resultadoMenor[1])
            grupo.append(resultadoMenor[2])
            jaTemGrupo.append(resultadoMenor[1])
            jaTemGrupo.append(resultadoMenor[2])
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
			#verifica termo 1
                xx = np.where(np.logical_or(min(distance_matrix[t1,:]) == distance_matrix[t1,:], min(distance_matrix[:,t1]) == distance_matrix[:,t1]))
                if(distance_matrix[t1][xx[0][0]] < distance_matrix[xx[0][1]][t1]):
                    tt1 = [t1,xx[0][0]]
                else:
                    tt1= [xx[0][1],t1]

                print("tt1 %s "%tt1)

					#termo 2
                yy = np.where(np.logical_or(min(distance_matrix[t2,:]) == distance_matrix[t2,:], min(distance_matrix[:,t2]) == distance_matrix[:,t2]))
                if(distance_matrix[t2][yy[0][0]] < distance_matrix[yy[0][1]][t2]):
                    tt2 = [t2,yy[0][0]]
                else:
                    tt2= [yy[0][1],t2]

                print("tt2 %s "%tt2)

                #verfica se t1 ou t2 estah mais proximo de qualquer outro ponto
                if(distance_matrix[tt1[0]][tt1[1]] < distance_matrix[tt2[0]][tt2[1]]):
						#se t1 tiver o termo mais proximos o valor de distance_matrix[tt1[0]][tt1[1]] recebera 100
					# e todos os valores da linha t2 e da coluna t2 receberao 100
                    print("escolhido tt1")
                    print("t1 %s"%t1)
                    print("t2 %s"%t2)
                    distance_matrix[tt1[0]][tt1[1]] = 100
                    #teste
                    distance_matrix[tt1[1]][tt1[0]] = 100
                    distance_matrix[t2,:]=100
                    distance_matrix[:,t2]=100
                    v = np.where(np.isin(tt1, grupo, invert=True))
                    print("tt1 eh menor  - v %s"%v)
                    print("v[0][0] %s"%tt1[v[0][0]])
                    grupo.append(tt1[v[0][0]])
                    jaTemGrupo.append(tt1[v[0][0]])
                    t1 = tt1[0]
                    t2 = tt1[1]
                    #se a quantidade de membros do grupo for igual ao desejado, as colunas e linhas t1 tambem sao setadas para 100
                    if(len(grupo) == nMembers):
                        distance_matrix[t1,:]=100
                        distance_matrix[:,t1]=100
                        distance_matrix[:,tt1[v[0][0]]]=100
                        distance_matrix[tt1[v[0][0]],:]=100
                        distance_matrix[t2,:]=100
                        distance_matrix[:,t2]=100
                        #distance_matrix[:,tt2[v[0][0]]]=100
                        #distance_matrix[tt2[v[0][0]],:]=100
                else:
					#se t2 tiver o termo mais proximos o valor de distance_matrix[tt2[0]][tt2[1]] recebera 100
			# e todos os valores da linha t1 e da coluna t1 receberao 100
                    print("escolhido tt2")
                    print("t1 %s"%t1)
                    print("t2 %s"%t2)
                    distance_matrix[tt2[0]][tt2[1]] = 100
                    distance_matrix[tt2[1]][tt2[0]] = 100
                    distance_matrix[t1,:]=100
                    distance_matrix[:,t1]=100
                    print("grupo %s"%grupo)
                    print("np is in %s"%np.isin(tt2, grupo, invert=True))
                    v = np.where(np.isin(tt2, grupo, invert=True))
                    print("tt2 eh mnor - v %s"%v)
                    print("v[0][0] %s"%tt2[v[0][0]])
                    grupo.append(tt2[v[0][0]])
                    jaTemGrupo.append(tt2[v[0][0]])
                    t1 = tt2[0]
                    t2 = tt2[1]
                        #se a quantidade de membros do grupo for igual ao desejado as colunas e linhas t2 tb sao setadas para 100
                    if(len(grupo) == nMembers):
                        distance_matrix[t1,:]=100
                        distance_matrix[:,t1]=100
                        #distance_matrix[:,tt1[v[0][0]]]=100
                        #distance_matrix[tt1[v[0][0]],:]=100
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