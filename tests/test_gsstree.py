"""
Unit tests for GSSTree.py - GSS tree similarity algorithm
"""
import unittest
import numpy as np
import xml.etree.ElementTree as ET
from io import StringIO
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GSSTree import (
    breadth_first,
    sibling_matrix,
    pre_order,
    get_last_child_index,
    ancester_matrix,
    get_anc_sib_matrices,
    exact_trace,
    exact_matched_M_weightless_preorder,
    exact_matched_M_weightless_bfs,
    exact_gss_tree
)


class TestGSSTree(unittest.TestCase):
    """Test cases for GSSTree module"""

    def setUp(self):
        """Set up test fixtures"""
        # Create simple XML trees for testing
        self.simple_xml_str = """<?xml version="1.0"?>
<root>
    <child1>
        <grandchild1/>
    </child1>
    <child2/>
</root>"""
        
        self.simple_xml_str2 = """<?xml version="1.0"?>
<root>
    <child1>
        <grandchild1/>
    </child1>
    <child2>
        <grandchild2/>
    </child2>
</root>"""
        
        self.simple_tree = ET.ElementTree(ET.fromstring(self.simple_xml_str))
        self.simple_tree2 = ET.ElementTree(ET.fromstring(self.simple_xml_str2))
        
        # Create identical tree for self-similarity test
        self.identical_tree = ET.ElementTree(ET.fromstring(self.simple_xml_str))
        
        # Single node tree
        self.single_node_str = """<?xml version="1.0"?>
<root/>"""
        self.single_node_tree = ET.ElementTree(ET.fromstring(self.single_node_str))

    def test_breadth_first_simple(self):
        """Test breadth first traversal on simple tree"""
        root = self.simple_tree.getroot()
        nodes = breadth_first(root)
        
        # Check that nodes are returned
        self.assertIsInstance(nodes, list)
        self.assertGreater(len(nodes), 0)
        
        # Check structure: each node is a tuple of (tag, num_right_siblings)
        for node in nodes:
            self.assertIsInstance(node, tuple)
            self.assertEqual(len(node), 2)
            self.assertIsInstance(node[0], str)  # tag
            self.assertIsInstance(node[1], int)  # num_right_siblings

    def test_breadth_first_single_node(self):
        """Test breadth first traversal on single node"""
        root = self.single_node_tree.getroot()
        nodes = breadth_first(root)
        
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0][0], 'root')
        self.assertEqual(nodes[0][1], 0)  # No right siblings

    def test_sibling_matrix_simple(self):
        """Test sibling matrix generation"""
        root = self.simple_tree.getroot()
        nodes = breadth_first(root)
        sib_M = sibling_matrix(nodes)
        
        # Check matrix shape
        n = len(nodes)
        self.assertEqual(sib_M.shape, (n, n))
        
        # Check matrix is numpy array
        self.assertIsInstance(sib_M, np.ndarray)
        
        # Check matrix contains only 0s and 1s
        unique_values = np.unique(sib_M)
        self.assertTrue(np.all(np.isin(unique_values, [0, 1])))

    def test_sibling_matrix_single_node(self):
        """Test sibling matrix for single node"""
        root = self.single_node_tree.getroot()
        nodes = breadth_first(root)
        sib_M = sibling_matrix(nodes)
        
        self.assertEqual(sib_M.shape, (1, 1))
        self.assertEqual(sib_M[0, 0], 0)

    def test_pre_order_simple(self):
        """Test pre-order traversal"""
        root = self.simple_tree.getroot()
        visited = []
        nodes = pre_order(root, visited)
        
        # Check that nodes are returned
        self.assertIsInstance(nodes, list)
        self.assertGreater(len(nodes), 0)
        
        # First node should be root
        self.assertEqual(nodes[0], 'root')
        
        # Check all nodes are strings (tags)
        for node in nodes:
            self.assertIsInstance(node, str)

    def test_pre_order_single_node(self):
        """Test pre-order traversal on single node"""
        root = self.single_node_tree.getroot()
        visited = []
        nodes = pre_order(root, visited)
        
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0], 'root')

    def test_get_last_child_index_simple(self):
        """Test last child index calculation"""
        root = self.simple_tree.getroot()
        visited = []
        pre_order_nodes = pre_order(root, visited)
        
        last_child_index = [0] * len(pre_order_nodes)
        result = get_last_child_index(root, 0, last_child_index)
        
        # Result should be total number of nodes
        self.assertEqual(result, len(pre_order_nodes))
        
        # All entries should be positive
        for idx in last_child_index:
            self.assertGreater(idx, 0)

    def test_get_last_child_index_single_node(self):
        """Test last child index for single node"""
        root = self.single_node_tree.getroot()
        visited = []
        pre_order_nodes = pre_order(root, visited)
        
        last_child_index = [0] * len(pre_order_nodes)
        result = get_last_child_index(root, 0, last_child_index)
        
        self.assertEqual(result, 1)
        self.assertEqual(last_child_index[0], 1)

    def test_ancester_matrix_simple(self):
        """Test ancestor matrix generation"""
        root = self.simple_tree.getroot()
        visited = []
        pre_order_nodes = pre_order(root, visited)
        
        last_child_index = [0] * len(pre_order_nodes)
        get_last_child_index(root, 0, last_child_index)
        
        anc_M = ancester_matrix(last_child_index)
        
        # Check matrix shape
        n = len(last_child_index)
        self.assertEqual(anc_M.shape, (n, n))
        
        # Check matrix is numpy array
        self.assertIsInstance(anc_M, np.ndarray)
        
        # Check matrix contains only 0s and 1s
        unique_values = np.unique(anc_M)
        self.assertTrue(np.all(np.isin(unique_values, [0, 1])))
        
        # Diagonal should be all 1s (node is ancestor of itself)
        self.assertTrue(np.all(np.diag(anc_M) == 1))

    def test_get_anc_sib_matrices(self):
        """Test getting both ancestor and sibling matrices"""
        anc_M, sib_M = get_anc_sib_matrices(self.simple_tree)
        
        # Check both matrices are returned
        self.assertIsInstance(anc_M, np.ndarray)
        self.assertIsInstance(sib_M, np.ndarray)
        
        # Check matrices are square and same size
        self.assertEqual(len(anc_M.shape), 2)
        self.assertEqual(len(sib_M.shape), 2)
        
        # Both matrices should have same number of rows
        # (though columns might differ due to different traversals)
        self.assertGreater(anc_M.shape[0], 0)
        self.assertGreater(sib_M.shape[0], 0)

    def test_exact_trace(self):
        """Test exact trace calculation"""
        # Create simple test matrices
        A = np.array([[1, 0], [1, 1]])
        B = np.array([[1, 0], [1, 1]])
        M = np.array([[1, 0], [0, 1]])
        
        trace = exact_trace(A, B, M)
        
        # Trace should be a number
        self.assertIsInstance(trace, (int, float, np.number))
        
        # For identical matrices with identity M, trace should be positive
        self.assertGreater(trace, 0)

    def test_exact_matched_M_weightless_preorder(self):
        """Test matched matrix in preorder"""
        M = exact_matched_M_weightless_preorder(self.simple_tree, self.simple_tree)
        
        # Check matrix is 2D numpy array
        self.assertIsInstance(M, np.ndarray)
        self.assertEqual(len(M.shape), 2)
        
        # Matrix should contain only 0s and 1s
        unique_values = np.unique(M)
        self.assertTrue(np.all(np.isin(unique_values, [0, 1])))
        
        # For identical trees, diagonal should have 1s
        min_dim = min(M.shape[0], M.shape[1])
        diagonal = np.array([M[i, i] for i in range(min_dim)])
        self.assertTrue(np.all(diagonal == 1))

    def test_exact_matched_M_weightless_bfs(self):
        """Test matched matrix in BFS order"""
        M = exact_matched_M_weightless_bfs(self.simple_tree, self.simple_tree)
        
        # Check matrix is 2D numpy array
        self.assertIsInstance(M, np.ndarray)
        self.assertEqual(len(M.shape), 2)
        
        # Matrix should contain only 0s and 1s
        unique_values = np.unique(M)
        self.assertTrue(np.all(np.isin(unique_values, [0, 1])))

    def test_exact_gss_tree_identical(self):
        """Test GSS tree similarity for identical trees"""
        sim = exact_gss_tree(self.simple_tree, self.identical_tree)
        
        # Similarity should be a number
        self.assertIsInstance(sim, (float, np.floating))
        
        # Identical trees should have similarity close to 1.0
        self.assertAlmostEqual(sim, 1.0, places=10)

    def test_exact_gss_tree_different(self):
        """Test GSS tree similarity for different trees"""
        sim = exact_gss_tree(self.simple_tree, self.simple_tree2)
        
        # Similarity should be a number
        self.assertIsInstance(sim, (float, np.floating))
        
        # Similarity should be between 0 and 1
        self.assertGreaterEqual(sim, 0.0)
        self.assertLessEqual(sim, 1.0)
        
        # Similar but not identical trees should have similarity less than 1
        self.assertLess(sim, 1.0)

    def test_exact_gss_tree_single_node(self):
        """Test GSS tree similarity for single node trees"""
        sim = exact_gss_tree(self.single_node_tree, self.single_node_tree)
        
        # Single identical node should have similarity 1.0
        self.assertAlmostEqual(sim, 1.0, places=10)

    def test_exact_gss_tree_symmetry(self):
        """Test that GSS tree similarity is symmetric"""
        sim1 = exact_gss_tree(self.simple_tree, self.simple_tree2)
        sim2 = exact_gss_tree(self.simple_tree2, self.simple_tree)
        
        # Similarity should be symmetric
        self.assertAlmostEqual(sim1, sim2, places=10)


if __name__ == '__main__':
    unittest.main()
