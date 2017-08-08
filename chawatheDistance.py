import numpy as np

def ldPair(xml_root, visited_nodes, level=0):
    visited_nodes.append((xml_root.tag,level))
    for child in xml_root:
        ldPair(child, visited_nodes, level+1)

    return visited_nodes

def change_cost( label1, label2):
	if label1 == label2:
		return 0
	else:
		return 1
def chawathe_distance(tree1, tree2):

	ldPairA = []
	ldPair(tree1.getroot(), ldPairA)
	
	ldPairB = []
	ldPair(tree2.getroot(), ldPairB)
	
	M = len(ldPairA)
	N = len(ldPairB)
	
	D = np.zeros((M+1, N+1))
	for i in range (1, M+1):
		D[i][0] = D[i-1][0] + 1
	for j in range (1, N+1):
		D[0][j] = D[0][j-1] + 1
		
	for i in range (1,M+1):
		for j in range (1,N+1):
			m1 = float('inf')
			m2 = float('inf')
			m3 = float('inf')
			if ldPairA[i-1][1] == ldPairB[j-1][1]:
				m1 = D[i-1][j-1] 
			if j==N or (ldPairB[j][1] <= ldPairA[i-1][1]):
				m2 = D[i-1][j] + 1
			if i==M or (ldPairA[i][1] <= ldPairB[j-1][1]):
				m3 = D[i][j-1] + 1
			D[i][j] = np.amin([m1,m2,m3])
	return D[M][N]
