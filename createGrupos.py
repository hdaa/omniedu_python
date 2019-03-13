def retornaMenor(distance_matrix, menorDistA,menorDistLinhaA,menorDistColA, relac):
	nCol = 0
	menorDist = menorDistA
	menorDistLinha = menorDistLinhaA
	for l in distance_matrix[menorDistLinhaA]:
		if l < menorDist and l !=0:
			menorDist = l
			menorDistCol = nCol
		nCol = nCol + 1

	if menorDist < menorDistA:
		#print("menorDistCol %s"%menorDistCol)
		relac.append(menorDistLinhaA)
		relac.append(menorDistCol)
		return retornaMenor(distance_matrix,menorDist, menorDistCol, menorDistLinha,relac)
	else:
		return [menorDistA, menorDistColA, menorDistLinhaA,relac]
	

def geraGrupos2(distance_matrix,nLinha):
	membrosNaoDisp =[]
	grupo = []
	gruposFormados = []
	menorDist = 100
	nLinha = 0
	menorDistCol=0
	menorDistLinha =0
	count = 0
	nMembers = 3

	grupo=[]
	nLinha = 0
	relac =[]
	for line in distance_matrix:
		menorDist = 100
		menorDistCol = 0
		grupo=[]
		g = []
		if nLinha not in membrosNaoDisp:
			while len(grupo) < nMembers and len(membrosNaoDisp) < len(distance_matrix[0]):
				g = retornaMenor(distance_matrix, menorDist,nLinha,menorDistCol,relac)
				if g[1] not in membrosNaoDisp and len(grupo) < nMembers:
					grupo.append(g[1])
					membrosNaoDisp.append(g[1])
				if g[2] not in membrosNaoDisp and len(grupo) < nMembers:
					grupo.append(g[2])
					membrosNaoDisp.append(g[2])
				for r in g[3]:
					if r not in membrosNaoDisp and len(grupo) < nMembers:
						membrosNaoDisp.append(r)
						grupo.append(r)
				#print("grupo %s"%grupo)
				distance_matrix[g[1]][g[2]]=0
				distance_matrix[g[2]][g[1]]=0
				#print("membrosNaoDisp %s"%membrosNaoDisp)
		nLinha = nLinha + 1
		#verfica se a coluna encontrada tem algo mais proximo
		if len(grupo) >0:
			gruposFormados.append(grupo)
	count = count+1
	print('gruposFormados %s'%gruposFormados)
	#print('distance_matrix %s'%distance_matrix)
	return gruposFormados

def geraGrupos(distance_matrix,nMembers):
	membrosNaoDisp =[]
	grupo = []
	gruposFormados = []
	menorDist = 100
	nLinha = 0
	nCol =  0
	menorDistCol=0
	for line in distance_matrix:
		if len(grupo) == nMembers:
			grupo=[]

		print('nLinha%s'%nLinha)
		if nLinha not in membrosNaoDisp:
			grupo.append(nLinha)
			membrosNaoDisp.append(nLinha)
			menorDist = 100
			while len(grupo) < nMembers and nCol < (len(line)-1):
				nCol =nLinha
				for l in line:
					if l < menorDist and l != 0:
						menorDist = l
						menorDistCol = nCol
					nCol = nCol + 1
				if menorDistCol not in grupo and menorDistCol not in membrosNaoDisp:
					grupo.append(menorDistCol)
					membrosNaoDisp.append(menorDistCol)
			if len(grupo) == nMembers:
				print('grupo %s'%grupo)
				gruposFormados.append(grupo)
			else:
				if nLinha == len(line)-1:
					gruposFormados.append(grupo)
		nLinha = nLinha + 1
		print('membrosNaoDisp %s'%membrosNaoDisp)
	print(gruposFormados)