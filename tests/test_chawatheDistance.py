"""
Comprehensive unit tests for chawatheDistance module
"""
import unittest
import numpy as np
import xml.etree.ElementTree as ET
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chawatheDistance import ldPair, change_cost, chawathe_distance


class TestChawatheDistance(unittest.TestCase):
    """Test suite for chawatheDistance module functions"""

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
        
        # Create another simple tree
        self.simple_xml_str2 = """<?xml version="1.0"?>
<root>
    <child1>
        <grandchild1/>
    </child1>
    <child2/>
</root>"""
        
        self.simple_tree2 = ET.ElementTree(ET.fromstring(self.simple_xml_str2))
        
        # Create a different tree
        self.different_xml_str = """<?xml version="1.0"?>
<root>
    <child1/>
    <child3/>
</root>"""
        
        self.different_tree = ET.ElementTree(ET.fromstring(self.different_xml_str))

    def test_ldPair(self):
        """Test ldPair function"""
        root = self.simple_tree.getroot()
        visited_nodes = []
        result = ldPair(root, visited_nodes)
        
        # Check that it returns a list
        self.assertIsInstance(result, list)
        
        # Check that we have nodes
        self.assertGreater(len(result), 0)
        
        # Check that each element is a tuple with (label, level)
        for node in result:
            self.assertIsInstance(node, tuple)
            self.assertEqual(len(node), 2)
            self.assertIsInstance(node[0], str)  # label
            self.assertIsInstance(node[1], int)  # level

    def test_ldPair_single_node(self):
        """Test ldPair with single node"""
        single_xml = ET.ElementTree(ET.fromstring("<root/>"))
        root = single_xml.getroot()
        visited_nodes = []
        result = ldPair(root, visited_nodes)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 'root')
        self.assertEqual(result[0][1], 0)

    def test_ldPair_level_tracking(self):
        """Test that ldPair tracks levels correctly"""
        root = self.simple_tree.getroot()
        visited_nodes = []
        result = ldPair(root, visited_nodes)
        
        # Root should be at level 0
        self.assertEqual(result[0][1], 0)
        
        # All levels should be non-negative
        for node in result:
            self.assertGreaterEqual(node[1], 0)

    def test_change_cost_same_labels(self):
        """Test change_cost with same labels"""
        cost = change_cost("label1", "label1")
        self.assertEqual(cost, 0)

    def test_change_cost_different_labels(self):
        """Test change_cost with different labels"""
        cost = change_cost("label1", "label2")
        self.assertEqual(cost, 1)

    def test_change_cost_empty_labels(self):
        """Test change_cost with empty labels"""
        cost1 = change_cost("", "")
        cost2 = change_cost("label", "")
        
        self.assertEqual(cost1, 0)
        self.assertEqual(cost2, 1)

    def test_chawathe_distance_identical_trees(self):
        """Test chawathe_distance with identical trees"""
        distance = chawathe_distance(self.simple_tree, self.simple_tree)
        
        # Check that distance is a number
        self.assertIsInstance(distance, (int, float, np.number))
        
        # Identical trees should have distance 0
        self.assertEqual(distance, 0)

    def test_chawathe_distance_different_trees(self):
        """Test chawathe_distance with different trees"""
        distance1 = chawathe_distance(self.simple_tree, self.simple_tree)
        distance2 = chawathe_distance(self.simple_tree, self.different_tree)
        
        # Different trees should have greater distance than identical trees
        self.assertGreaterEqual(distance2, distance1)
        
        # Distance should be non-negative
        self.assertGreaterEqual(distance2, 0)

    def test_chawathe_distance_single_nodes(self):
        """Test chawathe_distance with single node trees"""
        single_xml1 = ET.ElementTree(ET.fromstring("<root/>"))
        single_xml2 = ET.ElementTree(ET.fromstring("<root/>"))
        
        distance = chawathe_distance(single_xml1, single_xml2)
        
        self.assertEqual(distance, 0)

    def test_chawathe_distance_returns_numeric(self):
        """Test that chawathe_distance returns a numeric value"""
        distance = chawathe_distance(self.simple_tree, self.simple_tree2)
        
        self.assertIsInstance(distance, (int, float, np.number))


if __name__ == '__main__':
    unittest.main()
