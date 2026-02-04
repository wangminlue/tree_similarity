"""
Comprehensive unit tests for tree similarity methods.
Test coverage for all tree similarity algorithms and utility functions.
"""

import unittest
import numpy as np
import xml.etree.ElementTree as ET
from lxml import etree
import os

# Import modules to test
from GSSTree import (
    breadth_first, sibling_matrix, pre_order, get_last_child_index,
    ancester_matrix, get_anc_sib_matrices, exact_trace,
    exact_matched_M_weightless_preorder, exact_matched_M_weightless_bfs,
    exact_gss_tree
)
from XMLDistance import zhang_distance
from chawatheDistance import chawathe_distance, ldPair, change_cost
from get_XML_clusters import get_clusters, tree_exp, cal_stats


class TestGSSTreeFunctions(unittest.TestCase):
    """Test cases for GSSTree module functions."""
    
    def setUp(self):
        """Set up test XML trees."""
        self.test_xml1 = ET.parse('test_data/simple_tree1.xml')
        self.test_xml2 = ET.parse('test_data/simple_tree2.xml')
        self.identical_xml = ET.parse('test_data/identical_tree.xml')
        
    def test_pre_order(self):
        """Test pre-order traversal."""
        root = self.test_xml1.getroot()
        visited = []
        result = pre_order(root, visited)
        
        # Should contain all nodes
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
        self.assertEqual(result[0], 'root')
        
    def test_breadth_first(self):
        """Test breadth-first traversal."""
        root = self.test_xml1.getroot()
        result = breadth_first(root)
        
        # Should return list of tuples (tag, num_right_siblings)
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], tuple)
        self.assertEqual(result[0][0], 'root')
        
    def test_get_last_child_index(self):
        """Test getting last child indices."""
        root = self.test_xml1.getroot()
        visited = []
        pre_order_nodes = pre_order(root, visited)
        last_child_index = [0] * len(pre_order_nodes)
        
        result = get_last_child_index(root, 0, last_child_index)
        
        # Should return total number of nodes
        self.assertGreater(result, 0)
        self.assertEqual(result, len(pre_order_nodes))
        
    def test_ancester_matrix(self):
        """Test ancestor matrix generation."""
        last_childs = [3, 1, 1, 1]
        result = ancester_matrix(last_childs)
        
        # Should be a square matrix
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape[0], len(last_childs))
        self.assertEqual(result.shape[1], len(last_childs))
        
    def test_sibling_matrix(self):
        """Test sibling matrix generation."""
        nodes = [('root', 2), ('child1', 1), ('child2', 0)]
        result = sibling_matrix(nodes)
        
        # Should be a square matrix
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape[0], len(nodes))
        self.assertEqual(result.shape[1], len(nodes))
        
    def test_get_anc_sib_matrices(self):
        """Test getting ancestor and sibling matrices."""
        anc_M, sib_M = get_anc_sib_matrices(self.test_xml1)
        
        # Both should be numpy arrays
        self.assertIsInstance(anc_M, np.ndarray)
        self.assertIsInstance(sib_M, np.ndarray)
        # Should be square matrices
        self.assertEqual(anc_M.shape[0], anc_M.shape[1])
        self.assertEqual(sib_M.shape[0], sib_M.shape[1])
        
    def test_exact_matched_M_weightless_preorder(self):
        """Test exact match matrix for preorder."""
        M = exact_matched_M_weightless_preorder(self.test_xml1, self.test_xml2)
        
        # Should be a matrix
        self.assertIsInstance(M, np.ndarray)
        # Should have 2 dimensions
        self.assertEqual(len(M.shape), 2)
        # All values should be 0 or 1
        self.assertTrue(np.all((M == 0) | (M == 1)))
        
    def test_exact_matched_M_weightless_bfs(self):
        """Test exact match matrix for BFS."""
        M = exact_matched_M_weightless_bfs(self.test_xml1, self.test_xml2)
        
        # Should be a matrix
        self.assertIsInstance(M, np.ndarray)
        # Should have 2 dimensions
        self.assertEqual(len(M.shape), 2)
        # All values should be 0 or 1
        self.assertTrue(np.all((M == 0) | (M == 1)))
        
    def test_exact_trace(self):
        """Test exact trace calculation."""
        A = np.array([[1, 0], [0, 1]])
        B = np.array([[1, 0], [0, 1]])
        M = np.array([[1, 0], [0, 1]])
        
        result = exact_trace(A, B, M)
        
        # Should return a numeric value
        self.assertIsInstance(result, (int, float, np.number))
        
    def test_exact_gss_tree_identical(self):
        """Test GSS tree similarity for identical trees."""
        sim = exact_gss_tree(self.test_xml1, self.identical_xml)
        
        # Similarity should be high for identical trees
        self.assertIsInstance(sim, (float, np.floating))
        self.assertGreaterEqual(sim, 0.9)
        self.assertLessEqual(sim, 1.0)
        
    def test_exact_gss_tree_different(self):
        """Test GSS tree similarity for different trees."""
        sim = exact_gss_tree(self.test_xml1, self.test_xml2)
        
        # Similarity should be between 0 and 1
        self.assertIsInstance(sim, (float, np.floating))
        self.assertGreaterEqual(sim, 0.0)
        self.assertLessEqual(sim, 1.0)


class TestChawatheDistance(unittest.TestCase):
    """Test cases for Chawathe distance module."""
    
    def setUp(self):
        """Set up test XML trees."""
        self.test_xml1 = etree.parse('test_data/simple_tree1.xml')
        self.test_xml2 = etree.parse('test_data/simple_tree2.xml')
        self.identical_xml = etree.parse('test_data/identical_tree.xml')
        
    def test_ldPair(self):
        """Test label-depth pair generation."""
        root = self.test_xml1.getroot()
        visited = []
        result = ldPair(root, visited)
        
        # Should return list of (tag, level) tuples
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], tuple)
        self.assertEqual(len(result[0]), 2)
        
    def test_change_cost_equal(self):
        """Test change cost for equal labels."""
        result = change_cost('label1', 'label1')
        self.assertEqual(result, 0)
        
    def test_change_cost_different(self):
        """Test change cost for different labels."""
        result = change_cost('label1', 'label2')
        self.assertEqual(result, 1)
        
    def test_chawathe_distance_identical(self):
        """Test Chawathe distance for identical trees."""
        distance = chawathe_distance(self.test_xml1, self.identical_xml)
        
        # Distance should be 0 for identical trees
        self.assertEqual(distance, 0.0)
        
    def test_chawathe_distance_different(self):
        """Test Chawathe distance for different trees."""
        distance = chawathe_distance(self.test_xml1, self.test_xml2)
        
        # Distance should be positive for different trees
        self.assertGreater(distance, 0.0)


class TestXMLDistance(unittest.TestCase):
    """Test cases for Zhang distance (XMLDistance module)."""
    
    def setUp(self):
        """Set up test XML trees."""
        self.test_xml1 = ET.parse('test_data/simple_tree1.xml')
        self.test_xml2 = ET.parse('test_data/simple_tree2.xml')
        self.identical_xml = ET.parse('test_data/identical_tree.xml')
        
    def test_zhang_distance_identical(self):
        """Test Zhang distance for identical trees."""
        distance = zhang_distance(self.test_xml1, self.identical_xml)
        
        # Distance should be 0 for identical trees
        self.assertEqual(distance, 0)
        
    def test_zhang_distance_different(self):
        """Test Zhang distance for different trees."""
        distance = zhang_distance(self.test_xml1, self.test_xml2)
        
        # Distance should be positive for different trees
        self.assertGreater(distance, 0)


class TestGetXMLClusters(unittest.TestCase):
    """Test cases for get_XML_clusters module."""
    
    def test_cal_stats(self):
        """Test statistics calculation."""
        # Sample result pairs: (similarity, is_matched)
        result_pairs = [
            (0.9, True),
            (0.8, True),
            (0.7, False),
            (0.6, True),
            (0.5, False)
        ]
        
        ave_pre, max_fscore = cal_stats(result_pairs)
        
        # Should return numeric values
        self.assertIsInstance(ave_pre, float)
        self.assertIsInstance(max_fscore, float)
        # Values should be between 0 and 1
        self.assertGreaterEqual(ave_pre, 0.0)
        self.assertLessEqual(ave_pre, 1.0)
        self.assertGreaterEqual(max_fscore, 0.0)
        self.assertLessEqual(max_fscore, 1.0)
        
    def test_get_clusters(self):
        """Test getting clusters from directory."""
        # Use the real data directory
        path = './realworld_xml/'
        if os.path.exists(path):
            result = get_clusters(path)
            
            # Should return list of tuples
            self.assertIsInstance(result, list)
            if len(result) > 0:
                self.assertIsInstance(result[0], tuple)
                self.assertEqual(len(result[0]), 3)


class TestTreeExpWithModels(unittest.TestCase):
    """Test tree_exp function with different models."""
    
    def setUp(self):
        """Set up test data."""
        self.xml1 = etree.parse('test_data/simple_tree1.xml')
        self.xml2 = etree.parse('test_data/simple_tree2.xml')
        self.test_data = [
            (self.xml1, 'test1.xml', 'cluster1'),
            (self.xml2, 'test2.xml', 'cluster2')
        ]
        
    def test_tree_exp_gss_model(self):
        """Test tree_exp with GSS model."""
        print("\n" + "="*60)
        print("Testing GSS Model")
        print("="*60)
        ave_pre, max_fscore = tree_exp(self.test_data, method='gss')
        
        # Should return numeric values
        self.assertIsInstance(ave_pre, float)
        self.assertIsInstance(max_fscore, float)
        
    def test_tree_exp_zhang_model(self):
        """Test tree_exp with Zhang model."""
        print("\n" + "="*60)
        print("Testing Zhang Model")
        print("="*60)
        ave_pre, max_fscore = tree_exp(self.test_data, method='zhang')
        
        # Should return numeric values
        self.assertIsInstance(ave_pre, float)
        self.assertIsInstance(max_fscore, float)
        
    def test_tree_exp_chawathe_model(self):
        """Test tree_exp with Chawathe model."""
        print("\n" + "="*60)
        print("Testing Chawathe Model")
        print("="*60)
        ave_pre, max_fscore = tree_exp(self.test_data, method='chawathe')
        
        # Should return numeric values
        self.assertIsInstance(ave_pre, float)
        self.assertIsInstance(max_fscore, float)


if __name__ == '__main__':
    # Run tests with verbose output
    print("\n" + "="*60)
    print("COMPREHENSIVE UNIT TEST SUITE")
    print("Testing Tree Similarity Algorithms")
    print("="*60 + "\n")
    
    unittest.main(verbosity=2)
