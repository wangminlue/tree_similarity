"""
Comprehensive unit tests for GSSTree.py module.
Tests all functions related to tree similarity computation using GSS algorithm.
"""

import unittest
import numpy as np
import xml.etree.ElementTree as ET
import os
import sys

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from GSSTree import (
    breadth_first, sibling_matrix, pre_order, get_last_child_index,
    ancester_matrix, get_anc_sib_matrices, exact_trace,
    exact_matched_M_weightless_preorder, exact_matched_M_weightless_bfs,
    exact_gss_tree
)


class TestBreadthFirst(unittest.TestCase):
    """Test breadth_first function"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    
    def test_breadth_first_simple_tree(self):
        """Test breadth-first traversal on a simple tree"""
        xml = ET.parse(os.path.join(self.test_data_dir, 'simple_tree1.xml'))
        root = xml.getroot()
        nodes = breadth_first(root)
        
        # Check that nodes is a list of tuples
        self.assertIsInstance(nodes, list)
        self.assertTrue(all(isinstance(node, tuple) for node in nodes))
        
        # Check that first element is the root
        self.assertEqual(nodes[0][0], 'root')
        
        # Check the structure
        tags = [node[0] for node in nodes]
        self.assertIn('child1', tags)
        self.assertIn('child2', tags)
    
    def test_breadth_first_single_node(self):
        """Test breadth-first traversal on a tree with single node"""
        xml_str = '<?xml version="1.0"?><single/>'
        root = ET.fromstring(xml_str)
        nodes = breadth_first(root)
        
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0][0], 'single')
        self.assertEqual(nodes[0][1], 0)


class TestSiblingMatrix(unittest.TestCase):
    """Test sibling_matrix function"""
    
    def test_sibling_matrix_simple(self):
        """Test sibling matrix generation"""
        # Create mock nodes with (tag, num_right_siblings)
        nodes = [('root', 0), ('child1', 1), ('child2', 0)]
        sib_M = sibling_matrix(nodes)
        
        # Check matrix shape
        self.assertEqual(sib_M.shape, (3, 3))
        
        # Check that it's a numpy array
        self.assertIsInstance(sib_M, np.ndarray)
        
        # Check diagonal and properties
        self.assertTrue(np.all(sib_M >= 0))
    
    def test_sibling_matrix_empty(self):
        """Test sibling matrix with empty nodes"""
        nodes = []
        sib_M = sibling_matrix(nodes)
        self.assertEqual(sib_M.shape, (0, 0))


class TestPreOrder(unittest.TestCase):
    """Test pre_order function"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    
    def test_pre_order_traversal(self):
        """Test pre-order traversal"""
        xml = ET.parse(os.path.join(self.test_data_dir, 'simple_tree1.xml'))
        root = xml.getroot()
        visited = []
        result = pre_order(root, visited)
        
        # Check that result is a list
        self.assertIsInstance(result, list)
        
        # Check that root is first
        self.assertEqual(result[0], 'root')
        
        # Check all nodes are present
        self.assertIn('child1', result)
        self.assertIn('child2', result)
    
    def test_pre_order_single_node(self):
        """Test pre-order traversal on single node"""
        xml_str = '<?xml version="1.0"?><single/>'
        root = ET.fromstring(xml_str)
        visited = []
        result = pre_order(root, visited)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'single')


class TestGetLastChildIndex(unittest.TestCase):
    """Test get_last_child_index function"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    
    def test_get_last_child_index(self):
        """Test last child index calculation"""
        xml = ET.parse(os.path.join(self.test_data_dir, 'simple_tree1.xml'))
        root = xml.getroot()
        
        # Get pre-order nodes first
        visited = []
        pre_order_nodes = pre_order(root, visited)
        
        last_child_index = [0] * len(pre_order_nodes)
        num_nodes = get_last_child_index(root, 0, last_child_index)
        
        # Check return value
        self.assertIsInstance(num_nodes, int)
        self.assertGreater(num_nodes, 0)
        
        # Check that last_child_index is updated
        self.assertTrue(any(val > 0 for val in last_child_index))
    
    def test_get_last_child_index_single_node(self):
        """Test with single node"""
        xml_str = '<?xml version="1.0"?><single/>'
        root = ET.fromstring(xml_str)
        
        last_child_index = [0]
        num_nodes = get_last_child_index(root, 0, last_child_index)
        
        self.assertEqual(num_nodes, 1)
        self.assertEqual(last_child_index[0], 1)


class TestAncesterMatrix(unittest.TestCase):
    """Test ancester_matrix function"""
    
    def test_ancester_matrix_simple(self):
        """Test ancestor matrix generation"""
        last_childs = [3, 1, 1]  # Mock data
        anc_M = ancester_matrix(last_childs)
        
        # Check shape
        self.assertEqual(anc_M.shape, (3, 3))
        
        # Check it's a numpy array
        self.assertIsInstance(anc_M, np.ndarray)
        
        # Check properties
        self.assertTrue(np.all(anc_M >= 0))
        self.assertTrue(np.all(anc_M <= 1))
    
    def test_ancester_matrix_empty(self):
        """Test with empty input"""
        last_childs = []
        anc_M = ancester_matrix(last_childs)
        self.assertEqual(anc_M.shape, (0, 0))


class TestGetAncSibMatrices(unittest.TestCase):
    """Test get_anc_sib_matrices function"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    
    def test_get_anc_sib_matrices(self):
        """Test getting both ancestor and sibling matrices"""
        xml = ET.parse(os.path.join(self.test_data_dir, 'simple_tree1.xml'))
        anc_M, sib_M = get_anc_sib_matrices(xml)
        
        # Check both are numpy arrays
        self.assertIsInstance(anc_M, np.ndarray)
        self.assertIsInstance(sib_M, np.ndarray)
        
        # Check dimensions
        self.assertEqual(anc_M.shape[0], anc_M.shape[1])
        self.assertEqual(sib_M.shape[0], sib_M.shape[1])
        
        # Check same size
        self.assertEqual(anc_M.shape[0], sib_M.shape[0])


class TestExactTrace(unittest.TestCase):
    """Test exact_trace function"""
    
    def test_exact_trace_simple(self):
        """Test trace computation"""
        A = np.array([[1, 0], [0, 1]])
        B = np.array([[1, 0], [0, 1]])
        M = np.array([[1, 0], [0, 1]])
        
        trace = exact_trace(A, B, M)
        
        # Check result is a number
        self.assertIsInstance(trace, (int, float, np.number))
    
    def test_exact_trace_zeros(self):
        """Test with zero matrices"""
        A = np.zeros((2, 2))
        B = np.zeros((2, 2))
        M = np.zeros((2, 2))
        
        trace = exact_trace(A, B, M)
        self.assertEqual(trace, 0)


class TestExactMatchedM(unittest.TestCase):
    """Test exact_matched_M functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    
    def test_exact_matched_M_weightless_preorder(self):
        """Test preorder matching matrix"""
        xml1 = ET.parse(os.path.join(self.test_data_dir, 'simple_tree1.xml'))
        xml2 = ET.parse(os.path.join(self.test_data_dir, 'simple_tree2.xml'))
        
        M = exact_matched_M_weightless_preorder(xml1, xml2)
        
        # Check it's a numpy array
        self.assertIsInstance(M, np.ndarray)
        
        # Check values are 0 or 1
        self.assertTrue(np.all((M == 0) | (M == 1)))
    
    def test_exact_matched_M_weightless_bfs(self):
        """Test BFS matching matrix"""
        xml1 = ET.parse(os.path.join(self.test_data_dir, 'simple_tree1.xml'))
        xml2 = ET.parse(os.path.join(self.test_data_dir, 'simple_tree2.xml'))
        
        M = exact_matched_M_weightless_bfs(xml1, xml2)
        
        # Check it's a numpy array
        self.assertIsInstance(M, np.ndarray)
        
        # Check values are 0 or 1
        self.assertTrue(np.all((M == 0) | (M == 1)))


class TestExactGSSTree(unittest.TestCase):
    """Test exact_gss_tree function (main similarity computation)"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    
    def test_exact_gss_tree_identical(self):
        """Test GSS similarity between identical trees"""
        xml1 = ET.parse(os.path.join(self.test_data_dir, 'identical_tree.xml'))
        xml2 = ET.parse(os.path.join(self.test_data_dir, 'identical_tree.xml'))
        
        sim = exact_gss_tree(xml1, xml2)
        
        # Check result is a float
        self.assertIsInstance(sim, (float, np.floating))
        
        # Identical trees should have similarity close to 1.0
        self.assertAlmostEqual(sim, 1.0, places=5)
    
    def test_exact_gss_tree_different(self):
        """Test GSS similarity between different trees"""
        xml1 = ET.parse(os.path.join(self.test_data_dir, 'simple_tree1.xml'))
        xml2 = ET.parse(os.path.join(self.test_data_dir, 'simple_tree2.xml'))
        
        sim = exact_gss_tree(xml1, xml2)
        
        # Check result is a float
        self.assertIsInstance(sim, (float, np.floating))
        
        # Similarity should be between 0 and 1
        self.assertGreaterEqual(sim, 0)
        self.assertLessEqual(sim, 1.0)
    
    def test_exact_gss_tree_with_self(self):
        """Test GSS similarity of tree with itself"""
        xml = ET.parse(os.path.join(self.test_data_dir, 'simple_tree1.xml'))
        
        sim = exact_gss_tree(xml, xml)
        
        # Tree with itself should have similarity of 1.0
        self.assertAlmostEqual(sim, 1.0, places=5)


if __name__ == '__main__':
    unittest.main()
