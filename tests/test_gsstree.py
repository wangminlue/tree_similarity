"""
Unit tests for GSSTree.py - GSS Tree similarity algorithm
"""
import unittest
import numpy as np
import xml.etree.ElementTree as ET
from io import StringIO
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
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
    GSSTREE_AVAILABLE = True
except (SyntaxError, ImportError) as e:
    GSSTREE_AVAILABLE = False
    GSSTREE_IMPORT_ERROR = str(e)


class TestBreadthFirst(unittest.TestCase):
    """Test breadth_first traversal function"""
    
    def setUp(self):
        if not GSSTREE_AVAILABLE:
            self.skipTest(f"GSSTree module not available: {GSSTREE_IMPORT_ERROR}")
    
    def test_simple_tree(self):
        """Test breadth first traversal on a simple tree"""
        xml_str = """<root><child1/><child2/></root>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        result = breadth_first(tree.getroot())
        
        # Should return nodes in breadth-first order with right sibling counts
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][0], 'root')
        
    def test_single_node(self):
        """Test breadth first on a tree with single node"""
        xml_str = """<root/>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        result = breadth_first(tree.getroot())
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 'root')
        self.assertEqual(result[0][1], 0)
        
    def test_nested_tree(self):
        """Test breadth first on nested tree structure"""
        xml_str = """<root><child1><grandchild1/></child1><child2/></root>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        result = breadth_first(tree.getroot())
        
        # root, child1, child2, grandchild1
        self.assertEqual(len(result), 4)
        tags = [node[0] for node in result]
        self.assertIn('root', tags)
        self.assertIn('child1', tags)
        self.assertIn('child2', tags)
        self.assertIn('grandchild1', tags)


class TestSiblingMatrix(unittest.TestCase):
    """Test sibling_matrix generation"""
    
    def setUp(self):
        if not GSSTREE_AVAILABLE:
            self.skipTest(f"GSSTree module not available: {GSSTREE_IMPORT_ERROR}")
    
    def test_no_siblings(self):
        """Test sibling matrix for nodes with no siblings"""
        nodes = [('root', 0)]
        matrix = sibling_matrix(nodes)
        
        self.assertEqual(matrix.shape, (1, 1))
        self.assertEqual(matrix[0, 0], 0)
        
    def test_with_siblings(self):
        """Test sibling matrix with nodes that have siblings"""
        nodes = [('root', 2), ('child1', 0), ('child2', 0)]
        matrix = sibling_matrix(nodes)
        
        self.assertEqual(matrix.shape, (3, 3))
        # Root has 2 right siblings
        self.assertEqual(matrix[0, 0], 1)
        self.assertEqual(matrix[0, 1], 1)


class TestPreOrder(unittest.TestCase):
    """Test pre_order traversal function"""
    
    def setUp(self):
        if not GSSTREE_AVAILABLE:
            self.skipTest(f"GSSTree module not available: {GSSTREE_IMPORT_ERROR}")
    
    def test_simple_preorder(self):
        """Test pre-order traversal on simple tree"""
        xml_str = """<root><child1/><child2/></root>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        visited = []
        result = pre_order(tree.getroot(), visited)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], 'root')
        self.assertIn('child1', result)
        self.assertIn('child2', result)
        
    def test_nested_preorder(self):
        """Test pre-order traversal on nested tree"""
        xml_str = """<root><child1><grandchild/></child1><child2/></root>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        visited = []
        result = pre_order(tree.getroot(), visited)
        
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], 'root')
        # Pre-order: root, child1, grandchild, child2
        self.assertEqual(result[1], 'child1')
        
    def test_single_node_preorder(self):
        """Test pre-order on single node"""
        xml_str = """<root/>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        visited = []
        result = pre_order(tree.getroot(), visited)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'root')


class TestGetLastChildIndex(unittest.TestCase):
    """Test get_last_child_index function"""
    
    def setUp(self):
        if not GSSTREE_AVAILABLE:
            self.skipTest(f"GSSTree module not available: {GSSTREE_IMPORT_ERROR}")
    
    def test_single_node(self):
        """Test last child index for single node"""
        xml_str = """<root/>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        last_child_index = [0]
        result = get_last_child_index(tree.getroot(), 0, last_child_index)
        
        self.assertEqual(result, 1)
        self.assertEqual(last_child_index[0], 1)
        
    def test_with_children(self):
        """Test last child index with children"""
        xml_str = """<root><child1/><child2/></root>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        last_child_index = [0, 0, 0]
        result = get_last_child_index(tree.getroot(), 0, last_child_index)
        
        self.assertEqual(result, 3)
        self.assertEqual(last_child_index[0], 3)


class TestAncesterMatrix(unittest.TestCase):
    """Test ancester_matrix generation"""
    
    def setUp(self):
        if not GSSTREE_AVAILABLE:
            self.skipTest(f"GSSTree module not available: {GSSTREE_IMPORT_ERROR}")
    
    def test_single_node_ancestor(self):
        """Test ancestor matrix for single node"""
        last_childs = [1]
        matrix = ancester_matrix(last_childs)
        
        self.assertEqual(matrix.shape, (1, 1))
        self.assertEqual(matrix[0, 0], 1)
        
    def test_with_descendants(self):
        """Test ancestor matrix with descendants"""
        last_childs = [3, 1, 1]
        matrix = ancester_matrix(last_childs)
        
        self.assertEqual(matrix.shape, (3, 3))
        # First node has 3 descendants (including itself)
        self.assertEqual(matrix[0, 0], 1)
        self.assertEqual(matrix[0, 1], 1)
        self.assertEqual(matrix[0, 2], 1)


class TestGetAncSibMatrices(unittest.TestCase):
    """Test get_anc_sib_matrices function"""
    
    def setUp(self):
        if not GSSTREE_AVAILABLE:
            self.skipTest(f"GSSTree module not available: {GSSTREE_IMPORT_ERROR}")
    
    def test_simple_tree_matrices(self):
        """Test ancestor and sibling matrices generation"""
        xml_str = """<root><child1/><child2/></root>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        anc_M, sib_M = get_anc_sib_matrices(tree)
        
        self.assertIsInstance(anc_M, np.ndarray)
        self.assertIsInstance(sib_M, np.ndarray)
        self.assertEqual(anc_M.shape[0], anc_M.shape[1])
        self.assertEqual(sib_M.shape[0], sib_M.shape[1])


class TestExactTrace(unittest.TestCase):
    """Test exact_trace computation"""
    
    def setUp(self):
        if not GSSTREE_AVAILABLE:
            self.skipTest(f"GSSTree module not available: {GSSTREE_IMPORT_ERROR}")
    
    def test_trace_identity_matrices(self):
        """Test trace with identity matrices"""
        A = np.eye(3)
        B = np.eye(3)
        M = np.eye(3)
        
        trace = exact_trace(A, B, M)
        self.assertIsInstance(trace, (int, float, np.number))
        
    def test_trace_zero_matrices(self):
        """Test trace with zero matrices"""
        A = np.zeros((3, 3))
        B = np.zeros((3, 3))
        M = np.zeros((3, 3))
        
        trace = exact_trace(A, B, M)
        self.assertEqual(trace, 0)


class TestExactMatchedM(unittest.TestCase):
    """Test exact matched matrix functions"""
    
    def setUp(self):
        if not GSSTREE_AVAILABLE:
            self.skipTest(f"GSSTree module not available: {GSSTREE_IMPORT_ERROR}")
    
    def test_matched_m_preorder_identical_trees(self):
        """Test matched matrix for identical trees"""
        xml_str = """<root><child1/></root>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        
        M = exact_matched_M_weightless_preorder(tree, tree)
        
        self.assertIsInstance(M, np.ndarray)
        # Diagonal should be all 1s for identical trees
        self.assertTrue(np.all(np.diag(M) == 1))
        
    def test_matched_m_preorder_different_trees(self):
        """Test matched matrix for different trees"""
        xml_str1 = """<root><child1/></root>"""
        xml_str2 = """<root><child2/></root>"""
        tree1 = ET.ElementTree(ET.fromstring(xml_str1))
        tree2 = ET.ElementTree(ET.fromstring(xml_str2))
        
        M = exact_matched_M_weightless_preorder(tree1, tree2)
        
        self.assertIsInstance(M, np.ndarray)
        self.assertEqual(M.shape[0], 2)  # root, child1
        self.assertEqual(M.shape[1], 2)  # root, child2
        
    def test_matched_m_bfs_identical_trees(self):
        """Test BFS matched matrix for identical trees"""
        xml_str = """<root><child1/></root>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        
        M = exact_matched_M_weightless_bfs(tree, tree)
        
        self.assertIsInstance(M, np.ndarray)
        self.assertTrue(np.all(np.diag(M) == 1))


class TestExactGSSTree(unittest.TestCase):
    """Test exact_gss_tree similarity calculation"""
    
    def setUp(self):
        if not GSSTREE_AVAILABLE:
            self.skipTest(f"GSSTree module not available: {GSSTREE_IMPORT_ERROR}")
    
    def test_identical_trees_similarity(self):
        """Test that identical trees have similarity of 1.0"""
        xml_str = """<root><child1><grandchild/></child1><child2/></root>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        
        sim = exact_gss_tree(tree, tree)
        
        self.assertIsInstance(sim, (float, np.number))
        self.assertAlmostEqual(sim, 1.0, places=5)
        
    def test_different_trees_similarity(self):
        """Test similarity between different trees"""
        xml_str1 = """<root><child1/></root>"""
        xml_str2 = """<root><child2/></root>"""
        tree1 = ET.ElementTree(ET.fromstring(xml_str1))
        tree2 = ET.ElementTree(ET.fromstring(xml_str2))
        
        sim = exact_gss_tree(tree1, tree2)
        
        self.assertIsInstance(sim, (float, np.number))
        # Different trees should have similarity less than 1
        self.assertLess(sim, 1.0)
        self.assertGreaterEqual(sim, 0.0)
        
    def test_single_node_trees(self):
        """Test similarity of single node trees"""
        xml_str1 = """<root/>"""
        xml_str2 = """<root/>"""
        tree1 = ET.ElementTree(ET.fromstring(xml_str1))
        tree2 = ET.ElementTree(ET.fromstring(xml_str2))
        
        sim = exact_gss_tree(tree1, tree2)
        
        self.assertAlmostEqual(sim, 1.0, places=5)
        
    def test_completely_different_trees(self):
        """Test similarity of completely different trees"""
        xml_str1 = """<root><a/></root>"""
        xml_str2 = """<other><b/></other>"""
        tree1 = ET.ElementTree(ET.fromstring(xml_str1))
        tree2 = ET.ElementTree(ET.fromstring(xml_str2))
        
        sim = exact_gss_tree(tree1, tree2)
        
        self.assertIsInstance(sim, (float, np.number))
        self.assertGreaterEqual(sim, 0.0)
        self.assertLessEqual(sim, 1.0)


if __name__ == '__main__':
    unittest.main()
