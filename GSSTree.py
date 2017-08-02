import numpy as np
import xml.etree.ElementTree as ET
from collections import deque

def breadth_first (xml_root):
	nodes = []	
	#pair of node and number of right siblings
	stack = [(xml_root,0)]
	while stack :
	
		cur_node = stack[0]

		stack = stack[1:]
		num_right_sib = len(cur_node[0].getchildren())
		for child in cur_node[0]:
			stack.append((child, num_right_sib))
			num_right_sib -= 1
			
		nodes.append((cur_node[0].tag, cur_node[1]))
	return nodes

def sibling_matrix (nodes):
	l = len(nodes)
	sib_M = np.zeros((l,l))
	for node_index in range(l):
		num_right_sib = nodes[node_index][1]
		for i in range(num_right_sib):
			sib_M[node_index][node_index+i] = 1
	return sib_M
			

def pre_order (xml_root, visited_nodes):
	
	visited_nodes.append(xml_root.tag)
	for child in xml_root:
		pre_order(child, visited_nodes)
	
	return visited_nodes
	
	
	
def get_last_child_index (xml_root, index, last_child_index):
	
	#current node index
	temp = index
	#total children number
	nodes_num = 1
	for child in xml_root:
		index += 1
		#total nodes in subtree 'child'
		tree_nodes = get_last_child_index(child, index, last_child_index)
		nodes_num += tree_nodes
		#next child index
		index = index + tree_nodes -1
			
	last_child_index[temp] = nodes_num

	return nodes_num

def ancester_matrix (last_childs):
	
	l = len(last_childs)
	anc_M = np.zeros((l,l))	
	for i in range(l):
		for j in range(last_childs[i]):
			anc_M[i][i+j] = 1
			
	return anc_M

def get_anc_sib_matrices (xml):
	
	root = xml.getroot()
	
	visited_node = [] 
	pre_order_nodes = pre_order (root, visited_node)

	
	last_child_index = [0]*len(pre_order_nodes)
	get_last_child_index(root, 0, last_child_index)
	
	anc_M = ancester_matrix(last_child_index)
	
	nodes = breadth_first (root)
	sib_M = sibling_matrix(nodes)
	
	return anc_M, sib_M
	 
	
def exact_trace(A, B, M):
	

	M_transpose = M.copy()
	M_transpose = M_transpose.transpose()
	
	B_transpose = B.copy()
	B_transpose = B_transpose.transpose()

	
	output_matrix = np.matmul(np.matmul(np.matmul(A,M),B_transpose),M_transpose)
	
	trace_ab  = np.trace(output_matrix)
	#trace_ab = np.einsum("ik, km, jm, ij ->", A, M, B, M)
	
	return trace_ab	

def exact_matched_M_weightless_preorder(tree_A, tree_B):
	
	#tree_A pre order:
	visited_node = [] 
	pre_order_A = pre_order (tree_A.getroot(), visited_node)
	
	#tree_B pre order:
	visited_node = [] 
	pre_order_B = pre_order (tree_B.getroot(), visited_node)
	
	length_A = len(pre_order_A)
	length_B = len(pre_order_B)
		

	M = np.zeros((length_A, length_B))
	for i in range(length_A):
		for j in range(length_B):
			M[i,j] = float(pre_order_A[i] == pre_order_B[j])
	
	
	return M
	
def exact_matched_M_weightless_bfs(tree_A, tree_B):
	
	#tree_A breadth first:
	bfs_A = breadth_first (tree_A.getroot())
	
	#tree_B pre order:
	bfs_B = breadth_first (tree_B.getroot())
	
	length_A = len(bfs_A)
	length_B = len(bfs_B)
		

	M = np.zeros((length_A, length_B))
	for i in range(length_A):
		for j in range(length_B):
			M[i,j] = float(bfs_A[i][0] == bfs_B[j][0])
	
	
	return M
	
def exact_gss_tree (tree_A, tree_B):
	
	
	
	
	# anc_A, sib_A
	(anc_A, sib_A) = get_anc_sib_matrices(tree_A)
	

	# anc_B, sib_B
	(anc_B, sib_B) = get_anc_sib_matrices(tree_B)
	
	
	M_aa_preorder = exact_matched_M_weightless_preorder(tree_A, tree_A)
	
	M_bb_preorder = exact_matched_M_weightless_preorder(tree_B, tree_B)
	
	M_ab_preorder = exact_matched_M_weightless_preorder(tree_A, tree_B)
	
	M_aa_bfs = exact_matched_M_weightless_bfs(tree_A, tree_A)
	
	M_bb_bfs = exact_matched_M_weightless_bfs(tree_B, tree_B)
	
	M_ab_bfs = exact_matched_M_weightless_bfs(tree_A, tree_B)
	
	trace_ab = exact_trace(anc_A, anc_B, M_ab_preorder) + exact_trace(sib_A, sib_B, M_ab_bfs)
	trace_aa = exact_trace(anc_A, anc_A, M_aa_preorder) + exact_trace(sib_A, sib_A, M_aa_bfs)
	trace_bb = exact_trace(anc_B, anc_B, M_bb_preorder) + exact_trace(sib_B, sib_B, M_bb_bfs)
	

	sim = trace_ab/(np.sqrt(trace_aa*trace_bb))
	
	return sim	

if __name__ == "__main__":
	
	xml = ET.parse('OrdinaryIssuePage/102.xml')
	root = xml.getroot()
	
	visited_node = [] 
	pre_order_nodes = pre_order (root, visited_node)
	
	last_child_index = [0]*len(pre_order_nodes)
	get_last_child_index(root, 0, last_child_index)
	
	anc_matrix = ancester_matrix(last_child_index)
	anc_M = np.array( anc_matrix, copy='True')
	
	sib_M = sibling_matrix(anc_matrix)
	
	print sib_M
	print anc_M
	#return anc_matrix, sib_M
