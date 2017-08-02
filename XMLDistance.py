from  zss import simple_distance, Node
import xml.etree.ElementTree as ET


def printTree(root):
	tree_str = "("
	root_str = toString(root)
	tree_str += root_str
	
	for child in root:
		child_str =  ".addkid" + printTree(child)
		tree_str += child_str
	
	tree_str += ")"
	
	return tree_str
	 
def toString(xml_node):
	return "Node(\"" + xml_node.tag + "\")"
	

def zhang_distance(tree_A, tree_B):
	root_A = tree_A.getroot()
	root_B = tree_B.getroot()
	exec('tree_A ='+ printTree(root_A))	
	exec('tree_B ='+ printTree(root_B))
	d = simple_distance(tree_A, tree_B)
	
	return d
	
	

if __name__ == "__main__":
	
	xml_A = ET.parse('OrdinaryIssuePage/102.xml')
	root_A = xml_A.getroot()
	
	xml_B = ET.parse('OrdinaryIssuePage/111.xml')
	root_B = xml_B.getroot()
	
	
	exec('tree_A ='+ printTree(root_A))
	
	exec('tree_B ='+ printTree(root_B))
	
	d = simple_distance(tree_A, tree_B)
	
	print d
		
		
