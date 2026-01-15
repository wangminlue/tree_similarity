"""
Unit tests for chawatheDistance.py - Chawathe distance algorithm
"""
import unittest
import numpy as np
import xml.etree.ElementTree as ET
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chawatheDistance import ldPair, change_cost, chawathe_distance


class TestChawatheDistance(unittest.TestCase):
    """Test cases for chawatheDistance module"""

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
        
        # Create identical tree
        self.identical_tree = ET.ElementTree(ET.fromstring(self.simple_xml_str))
        
        # Single node tree
        self.single_node_str = """<?xml version="1.0"?>
<root/>"""
        self.single_node_tree = ET.ElementTree(ET.fromstring(self.single_node_str))

    def test_ldPair_simple(self):
        """Test ldPair function on simple tree"""
        root = self.simple_tree.getroot()
        visited_nodes = []
        result = ldPair(root, visited_nodes)
        
        # Check that nodes are returned
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        
        # Check structure: each node is a tuple of (tag, level)
        for node in result:
            self.assertIsInstance(node, tuple)
            self.assertEqual(len(node), 2)
            self.assertIsInstance(node[0], str)  # tag
            self.assertIsInstance(node[1], int)  # level
            self.assertGreaterEqual(node[1], 0)  # level should be non-negative

    def test_ldPair_single_node(self):
        """Test ldPair on single node"""
        root = self.single_node_tree.getroot()
        visited_nodes = []
        result = ldPair(root, visited_nodes)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 'root')
        self.assertEqual(result[0][1], 0)  # Root is at level 0

    def test_ldPair_levels(self):
        """Test that ldPair correctly assigns levels"""
        root = self.simple_tree.getroot()
        visited_nodes = []
        result = ldPair(root, visited_nodes)
        
        # First node (root) should be at level 0
        self.assertEqual(result[0][1], 0)
        
        # All levels should be non-negative and reasonable
        max_level = max(node[1] for node in result)
        self.assertGreater(max_level, 0)  # Tree has multiple levels
        self.assertLess(max_level, 10)  # Reasonable depth

    def test_change_cost_same_label(self):
        """Test change_cost for identical labels"""
        cost = change_cost('label1', 'label1')
        self.assertEqual(cost, 0)

    def test_change_cost_different_label(self):
        """Test change_cost for different labels"""
        cost = change_cost('label1', 'label2')
        self.assertEqual(cost, 1)

    def test_change_cost_empty_strings(self):
        """Test change_cost for empty strings"""
        cost = change_cost('', '')
        self.assertEqual(cost, 0)

    def test_chawathe_distance_identical(self):
        """Test Chawathe distance for identical trees"""
        distance = chawathe_distance(self.simple_tree, self.identical_tree)
        
        # Distance should be a number
        self.assertIsInstance(distance, (int, float, np.number))
        
        # Identical trees should have distance 0
        self.assertEqual(distance, 0)

    def test_chawathe_distance_different(self):
        """Test Chawathe distance for different trees"""
        distance = chawathe_distance(self.simple_tree, self.simple_tree2)
        
        # Distance should be a number
        self.assertIsInstance(distance, (int, float, np.number))
        
        # Different trees should have positive distance
        self.assertGreater(distance, 0)

    def test_chawathe_distance_single_node(self):
        """Test Chawathe distance for single node trees"""
        distance = chawathe_distance(self.single_node_tree, self.single_node_tree)
        
        # Identical single nodes should have distance 0
        self.assertEqual(distance, 0)

    def test_chawathe_distance_symmetry(self):
        """Test that Chawathe distance is symmetric"""
        distance1 = chawathe_distance(self.simple_tree, self.simple_tree2)
        distance2 = chawathe_distance(self.simple_tree2, self.simple_tree)
        
        # Distance should be symmetric
        self.assertEqual(distance1, distance2)

    def test_chawathe_distance_triangle_inequality(self):
        """Test triangle inequality property"""
        # Create a third tree
        xml_str3 = """<?xml version="1.0"?>
<root>
    <child1/>
</root>"""
        tree3 = ET.ElementTree(ET.fromstring(xml_str3))
        
        d12 = chawathe_distance(self.simple_tree, self.simple_tree2)
        d13 = chawathe_distance(self.simple_tree, tree3)
        d23 = chawathe_distance(self.simple_tree2, tree3)
        
        # Triangle inequality: d(A,C) <= d(A,B) + d(B,C)
        self.assertLessEqual(d13, d12 + d23)
        self.assertLessEqual(d23, d12 + d13)
        self.assertLessEqual(d12, d13 + d23)

    def test_chawathe_distance_non_negative(self):
        """Test that Chawathe distance is always non-negative"""
        distance = chawathe_distance(self.simple_tree, self.simple_tree2)
        self.assertGreaterEqual(distance, 0)


if __name__ == '__main__':
    unittest.main()
