import subprocess 


def chawathe_distance(file1, file2):

	string = 'xmldiff  '+file1+' '+file2
	p = subprocess.Popen([string], shell=True,  stdout=subprocess.PIPE)	
	lines = p.stdout.readlines()
	return len(lines)
		
if __name__ == "__main__":
	
	file1 = './realworld_xml/OrdinaryIssuePage/12.xml'
	file2 = './realworld_xml/OrdinaryIssuePage/12.xml'
	
	print chawathe_distance(file1,file2)
