import xml.etree.ElementTree as ET   
import subprocess 

def print_bracket_tree(xml_root):
    tree_str = "{"
    root_str = xml_root.tag
    tree_str += root_str

    for child in xml_root:
        child_str =  print_bracket_tree(child)
        tree_str += child_str

    tree_str += "}"

    return tree_str
    
def apted_distance(tree_A, tree_B):
	rootA = tree_A.getroot()
	rootB = tree_B.getroot()
	
	btreeA = print_bracket_tree(rootA)
	btreeB = print_bracket_tree(rootB)
	
	p = subprocess.check_output(['java','-jar','apted.jar', '-t',btreeA, btreeB])
	
	return float(p.strip())
	

if __name__ == "__main__":
	xml102 = ET.parse('./realworld_xml/OrdinaryIssuePage/102.xml')
	root = xml102.getroot()
	
	tree1 = print_bracket_tree(root)

	
	p = subprocess.check_output(['java','-jar','apted.jar', '-t',tree1, tree1])
	
	print (p.strip())


	
