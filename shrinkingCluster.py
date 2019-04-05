def colSum(matriz):
	naoZero = []
	resultMatrix=[]
	for j in range(0,len(matriz[0])):
		clsum = 0
		for i in range(0,len(matriz)):
			clsum = clsum + matriz[i][j]
		if clsum != 0:
			naoZero.append(j)
	montaLinha = []
	for linha in range(0,len(matriz)):
		for n in naoZero:
			montaLinha.append(matriz[linha][n])
		resultMatrix.append(montaLinha)
		montaLinha=[]
	return resultMatrix

def colSumMenor(matriz):
	for j in range(0,len(matriz[0])):
		if(sum(matriz[:,j])!=0):
			naoZero.append(j)
	montaLinha = []
	for linha in range(0,len(matriz)):
		for n in naoZero:
			montaLinha.append(matriz[linha][n])
		resultMatrix.append(montaLinha)
		montaLinha=[]
	return resultMatrix


## Parametros:
## data_matrix eh a matrix de similaridade
## w eh o numero minimo de membros em cada cluster
## k eh o maximo numero de clusters permitidos
## iter numero máximo de iteracoes
## random eh um inteiro especificando o numero de inicializações aleatorias
## Retorno:
## c - vetor n x 1 determinando quando ou não track e gravar o numero
##   de clusters restantes em cada iteracao
## a - matrix n x k indicanto o cluster de cada ponto
## score - indicador de convergencia
def SuperCluster(data_matrix, w,k, iter=10,random=1,Path=0):
	import numpy as np
	from random import randint
	from math import ceil
	Step = 1
	n = len(data_matrix[0])
	f= 0
	k = ceil(n/w)
	#
	#Generate a random AN×K0 (cluster assignment matrix)
	#
	x = np.asarray(np.zeros((n,k)))
	cluster = np.zeros((n,random))
	#b. Compute DS = 1 − 2S
	ds = 1 - 2*data_matrix
	np.fill_diagonal(ds,0)
	if Path==1:
		path= np.zeros((iter,random))
	for rs in range(0,random):
		step = Step
		linha =0
		tamanho = len(x[0])-1
		for y in x:
			for i in range(0,randint(0,tamanho)):
				x[linha][randint(0,k-1)]=1
			linha = linha +1
		i=0
		print("Iteration %s"%i)
		flag = 0
		while i< iter:
			#deletando colunas vazias. nao precisa
			#x = np.asarray(colSum(x))
			print("x %s"%x)
			#Permute the cluster membership that minimizes Function 2 the most: 
			#(a) Compute M = DSA
			ss = np.matmul(ds,x)
			print("ss %s"%ss)
			####
			if Path==1:
				path[i,rs]= len(x[0])
			kj = 0
			print("len x0 %s"%(len(x[0])))
			#remove clusters pequenos
			while kj <= (len(x[0])-1):
				print("kj %s"%kj)
				print("sumkj %s" %sum(x[:,kj]))
				if(sum(x[:,kj])) < w:
					xi = np.where(x[:,kj] == 1)[0]
					x = np.delete(x,kj,1) #deletando linha com poucos clusters
					print("x after delete columns %s"%x)
					ss = np.delete(ss,kj,1)
					print("ss after delete columns %s"%ss)
					if(len(ss) is 0):
						x[xi]=1
						flag=1
						break
					else:
						for ri in xi:
							minSri = min(ss[ri,:])
							x[ri, np.where(ss[ri,:]==minSri)]=1
					ss = np.matmul(ds,x)
				else:
					kj = kj + 1
			if(flag==1):
				break;
			else:
				#(b) Compute v by vi = min
				ms = []
				print("npmultiply %s"%np.multiply(ss,x))
				for o in range(0,len(ss)-1):
					ms.append(min(ss[o,:]) - sum(np.multiply(ss,x)[o,:]))
				print("ms %s"%ms)
				print("soma ms %s"%sum(ms))
				if(sum(ms)==0):#convergencia
					f=1
					break
				else:
					if step==1:
						xi=np.where(ms==max(ms))[0]
						print("xi %s"%xi)
						x[xi,:]=0
						selection=[]
						for h in xi:
							selection.append(np.where(ss[h,:]==min(ss[h,:])))
						print("selection ".join(map(str,selection)))
						#x[xi, np.where(ss[xi,:]==min(ss[xi,:]))]=1
						x[xi, selection]=1
						print("x apos selection %s "%x)
					else:
						mi= np.array(ms).argsort()[-n:][::-1]
						ms = np.asarray(ms)
						if sum(ms!=0) <= step:
							if step > 9:
								step=round(sum(ms!=0)/2)
							else:
								step=1
						xi = mi[0:step]
						x[xi,:]=0
						for ri in xi:
							x[ri, np.where(ss[ri,:]==min(ss[ri,:]))]=1
				i = i +1
				#print("\b\b\b\b")
				#print("%s"%i) #fim while iter
		fr=[]
		if rs==0:
			fr = sum((data_matrix-np.matmul(x,np.transpose(x)))**2)
		else:
			fr.append(sum((data_matrix-np.matmul(x,np.transpose(x)))**2))
		if Path==1:
			path[(i-1),rs]= len(x[0])
		if flag==1:
			cluster.fill(1)
		else:
			c=1
			for i in range(0,len(x[0])):
				cluster[x[:,i] != 0, rs] = c
				c = c +1
	return {"c":cluster, "a":x, "score":fr}









