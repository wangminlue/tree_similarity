"""
Comprehensive unit tests for GSSTree module
"""
import unittest
import numpy as np
import xml.etree.ElementTree as ET
from io import StringIO
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
    """Test suite for GSSTree module functions"""

    def setUp(self):
        """Set up test fixtures"""
        # Create simple test XML trees
        self.simple_xml_str = """<?xml version="1.0"?>
<root>
    <child1>
        <grandchild1/>
    </child1>
    <child2/>
</root>"""
        
        self.simple_tree = ET.ElementTree(ET.fromstring(self.simple_xml_str))
        
        # Create another simple tree for comparison
        self.simple_xml_str2 = """<?xml version="1.0"?>
<root>
    <child1>
        <grandchild1/>
    </child1>
    <child2/>
</root>"""
        
        self.simple_tree2 = ET.ElementTree(ET.fromstring(self.simple_xml_str2))
        
        # Create a different tree for comparison
        self.different_xml_str = """<?xml version="1.0"?>
<root>
    <child1/>
    <child2>
        <grandchild2/>
    </child2>
</root>"""
        
        self.different_tree = ET.ElementTree(ET.fromstring(self.different_xml_str))

    def test_breadth_first(self):
        """Test breadth_first function"""
        root = self.simple_tree.getroot()
        nodes = breadth_first(root)
        
        # Check that nodes is a list
        self.assertIsInstance(nodes, list)
        
        # Check that we have the correct number of nodes
        self.assertEqual(len(nodes), 4)  # root, child1, child2, grandchild1
        
        # Check that first node is root
        self.assertEqual(nodes[0][0], 'root')
        
        # Check that nodes contain tuples
        for node in nodes:
            self.assertIsInstance(node, tuple)
            self.assertEqual(len(node), 2)
            self.assertIsInstance(node[0], str)
            self.assertIsInstance(node[1], int)

    def test_breadth_first_single_node(self):
        """Test breadth_first with single node"""
        single_xml = ET.ElementTree(ET.fromstring("<root/>"))
        root = single_xml.getroot()
        nodes = breadth_first(root)
        
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0][0], 'root')

    def test_sibling_matrix(self):
        """Test sibling_matrix function"""
        root = self.simple_tree.getroot()
        nodes = breadth_first(root)
        sib_M = sibling_matrix(nodes)
        
        # Check that it's a numpy array
        self.assertIsInstance(sib_M, np.ndarray)
        
        # Check dimensions
        self.assertEqual(sib_M.shape[0], len(nodes))
        self.assertEqual(sib_M.shape[1], len(nodes))
        
        # Check that diagonal has 0 or 1
        for i in range(len(nodes)):
            self.assertIn(sib_M[i][i], [0, 1])

    def test_sibling_matrix_single_node(self):
        """Test sibling_matrix with single node"""
        single_xml = ET.ElementTree(ET.fromstring("<root/>"))
        root = single_xml.getroot()
        nodes = breadth_first(root)
        sib_M = sibling_matrix(nodes)
        
        self.assertEqual(sib_M.shape, (1, 1))
        self.assertEqual(sib_M[0][0], 0)

    def test_pre_order(self):
        """Test pre_order function"""
        root = self.simple_tree.getroot()
        visited_nodes = []
        result = pre_order(root, visited_nodes)
        
        # Check that it returns a list
        self.assertIsInstance(result, list)
        
        # Check that we have the correct number of nodes
        self.assertEqual(len(result), 4)
        
        # Check that first node is root
        self.assertEqual(result[0], 'root')
        
        # Check that all elements are strings
        for node in result:
            self.assertIsInstance(node, str)

    def test_pre_order_empty_list(self):
        """Test pre_order with empty list"""
        root = self.simple_tree.getroot()
        visited_nodes = []
        pre_order(root, visited_nodes)
        
        self.assertGreater(len(visited_nodes), 0)

    def test_get_last_child_index(self):
        """Test get_last_child_index function"""
        root = self.simple_tree.getroot()
        visited_nodes = []
        pre_order_nodes = pre_order(root, visited_nodes)
        
        last_child_index = [0] * len(pre_order_nodes)
        result = get_last_child_index(root, 0, last_child_index)
        
        # Check return value is the number of nodes in tree
        self.assertEqual(result, len(pre_order_nodes))
        
        # Check that last_child_index is updated
        self.assertEqual(len(last_child_index), len(pre_order_nodes))
        
        # Check that all values are positive
        for val in last_child_index:
            self.assertGreaterEqual(val, 1)

    def test_get_last_child_index_single_node(self):
        """Test get_last_child_index with single node"""
        single_xml = ET.ElementTree(ET.fromstring("<root/>"))
        root = single_xml.getroot()
        last_child_index = [0]
        result = get_last_child_index(root, 0, last_child_index)
        
        self.assertEqual(result, 1)
        self.assertEqual(last_child_index[0], 1)

    def test_ancester_matrix(self):
        """Test ancester_matrix function"""
        root = self.simple_tree.getroot()
        visited_nodes = []
        pre_order_nodes = pre_order(root, visited_nodes)
        
        last_child_index = [0] * len(pre_order_nodes)
        get_last_child_index(root, 0, last_child_index)
        
        anc_M = ancester_matrix(last_child_index)
        
        # Check that it's a numpy array
        self.assertIsInstance(anc_M, np.ndarray)
        
        # Check dimensions
        self.assertEqual(anc_M.shape[0], len(last_child_index))
        self.assertEqual(anc_M.shape[1], len(last_child_index))
        
        # Check that diagonal is 1 (node is ancestor of itself)
        for i in range(len(last_child_index)):
            self.assertEqual(anc_M[i][i], 1)

    def test_ancester_matrix_single_node(self):
        """Test ancester_matrix with single node"""
        last_child_index = [1]
        anc_M = ancester_matrix(last_child_index)
        
        self.assertEqual(anc_M.shape, (1, 1))
        self.assertEqual(anc_M[0][0], 1)

    def test_get_anc_sib_matrices(self):
        """Test get_anc_sib_matrices function"""
        anc_M, sib_M = get_anc_sib_matrices(self.simple_tree)
        
        # Check that both are numpy arrays
        self.assertIsInstance(anc_M, np.ndarray)
        self.assertIsInstance(sib_M, np.ndarray)
        
        # Check that both are square matrices
        self.assertEqual(anc_M.shape[0], anc_M.shape[1])
        self.assertEqual(sib_M.shape[0], sib_M.shape[1])
        
        # Check that both have same dimensions
        self.assertEqual(anc_M.shape, sib_M.shape)

    def test_exact_trace(self):
        """Test exact_trace function"""
        # Create simple test matrices
        A = np.array([[1, 0], [0, 1]])
        B = np.array([[1, 0], [0, 1]])
        M = np.array([[1, 0], [0, 1]])
        
        trace = exact_trace(A, B, M)
        
        # Check that trace is a number
        self.assertIsInstance(trace, (int, float, np.number))
        
        # Check that trace is non-negative
        self.assertGreaterEqual(trace, 0)

    def test_exact_trace_zero_matrices(self):
        """Test exact_trace with zero matrices"""
        A = np.zeros((2, 2))
        B = np.zeros((2, 2))
        M = np.zeros((2, 2))
        
        trace = exact_trace(A, B, M)
        self.assertEqual(trace, 0)

    def test_exact_matched_M_weightless_preorder(self):
        """Test exact_matched_M_weightless_preorder function"""
        M = exact_matched_M_weightless_preorder(self.simple_tree, self.simple_tree2)
        
        # Check that it's a numpy array
        self.assertIsInstance(M, np.ndarray)
        
        # Check that it has correct dimensions
        root1 = self.simple_tree.getroot()
        root2 = self.simple_tree2.getroot()
        visited1 = []
        visited2 = []
        pre_order(root1, visited1)
        pre_order(root2, visited2)
        
        self.assertEqual(M.shape[0], len(visited1))
        self.assertEqual(M.shape[1], len(visited2))
        
        # Check that values are 0 or 1
        unique_values = np.unique(M)
        for val in unique_values:
            self.assertIn(val, [0.0, 1.0])

    def test_exact_matched_M_weightless_preorder_identical_trees(self):
        """Test exact_matched_M_weightless_preorder with identical trees"""
        M = exact_matched_M_weightless_preorder(self.simple_tree, self.simple_tree)
        
        # For identical trees, diagonal should be all 1s
        self.assertTrue(np.all(np.diag(M) == 1.0))

    def test_exact_matched_M_weightless_bfs(self):
        """Test exact_matched_M_weightless_bfs function"""
        M = exact_matched_M_weightless_bfs(self.simple_tree, self.simple_tree2)
        
        # Check that it's a numpy array
        self.assertIsInstance(M, np.ndarray)
        
        # Check that values are 0 or 1
        unique_values = np.unique(M)
        for val in unique_values:
            self.assertIn(val, [0.0, 1.0])

    def test_exact_matched_M_weightless_bfs_identical_trees(self):
        """Test exact_matched_M_weightless_bfs with identical trees"""
        M = exact_matched_M_weightless_bfs(self.simple_tree, self.simple_tree)
        
        # For identical trees, diagonal should be all 1s
        self.assertTrue(np.all(np.diag(M) == 1.0))

    def test_exact_gss_tree(self):
        """Test exact_gss_tree function"""
        sim = exact_gss_tree(self.simple_tree, self.simple_tree2)
        
        # Check that similarity is a number
        self.assertIsInstance(sim, (int, float, np.number))
        
        # Check that similarity is between 0 and 1
        self.assertGreaterEqual(sim, 0)
        self.assertLessEqual(sim, 1)

    def test_exact_gss_tree_identical_trees(self):
        """Test exact_gss_tree with identical trees"""
        sim = exact_gss_tree(self.simple_tree, self.simple_tree)
        
        # Identical trees should have similarity close to 1
        self.assertAlmostEqual(sim, 1.0, places=5)

    def test_exact_gss_tree_different_trees(self):
        """Test exact_gss_tree with different trees"""
        sim1 = exact_gss_tree(self.simple_tree, self.simple_tree)
        sim2 = exact_gss_tree(self.simple_tree, self.different_tree)
        
        # Same trees should be more similar than different trees
        self.assertGreaterEqual(sim1, sim2)


if __name__ == '__main__':
    unittest.main()
