from os import listdir
#import xml.etree.ElementTree as ET
from lxml import etree
from GSSTree import exact_gss_tree
from XMLDistance import zhang_distance
from RTED import apted_distance
from XML_CHAWATHE import chawathe_distance

def get_clusters(path):

    xml_cluster_trip= []
    clusters_dir = listdir(path)
    for c_dir in clusters_dir:
        fullpath = path + c_dir
        files = listdir(fullpath)
        for xml in files:
            xml_path = fullpath + "/" + xml
            xml_tree = etree.parse(xml_path)
            xml_cluster_trip.append((xml_tree, xml_path, c_dir))

    return xml_cluster_trip


def tree_exp(xml_cluster_trip, method="gss"):

    result_pairs = []
    i = 0
    for xml1, xml1_file, cluster1 in xml_cluster_trip:
        for xml2, xml2_file, cluster2 in xml_cluster_trip:
			print i
			i += 1
			if method == "gss":
				sim = exact_gss_tree(xml1, xml2)
				matched = (cluster1 == cluster2)
				result_pairs.append((sim, matched))
			elif method =='zhang':
				sim = zhang_distance(xml1,xml2)
				matched = (cluster1==cluster2)
				result_pairs.append((sim,matched))
			elif method =='apted':
				sim = apted_distance(xml1,xml2)
				matched = (cluster1 == cluster2)
				result_pairs.append((sim,matched))
			elif method == 'chawathe':
				sim = chawathe_distance(xml1_file, xml2_file)
				matched = (cluster1 == cluster2)
				result_pairs.append((sim,matched))
			else:
				print 'no method found'
	
			
             

    ave_pre, max_fscore = cal_stats(result_pairs)

    return ave_pre, max_fscore


def cal_stats(result_pairs):
    sorted_pairs = sorted(result_pairs, key=lambda x: x[0], reverse=True)

    total_matched = sum([int(label) for _, label in sorted_pairs])

    matched_sofar = 0.0
    max_fscore = 0.0
    total_precision = 0.0
    total_f_score = 0.0
    for i in range(len(sorted_pairs)):
        pair = sorted_pairs[i]
        if(pair[1]):
            matched_sofar += 1.0
            current_precision = matched_sofar / (i + 1)
            current_recall = matched_sofar / total_matched
            current_fscore = 2 / (1 / current_precision + 1 / current_recall)
            if (current_fscore > max_fscore):
                max_fscore = current_fscore
            total_precision += current_precision

    #print("Average precision: {0} Max F1: {1}".format( total_precision/total_matched, max_fscore))

    return total_precision / total_matched, max_fscore

if __name__ == "__main__":

    path = './realworld_xml/'
    data = get_clusters(path)
    pre, recall = tree_exp(data, method='chawathe')

    print pre
    print recall
    # return anc_matrix, sib_M
