"""
Comprehensive unit tests for chawatheDistance.py module.
Tests the Chawathe distance algorithm for tree comparison.
"""

import unittest
import numpy as np
import xml.etree.ElementTree as ET
import os
import sys

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chawatheDistance import ldPair, change_cost, chawathe_distance


class TestLdPair(unittest.TestCase):
    """Test ldPair function (label-depth pairs)"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    
    def test_ldPair_simple_tree(self):
        """Test ldPair on a simple tree"""
        xml = ET.parse(os.path.join(self.test_data_dir, 'simple_tree1.xml'))
        root = xml.getroot()
        visited = []
        result = ldPair(root, visited)
        
        # Check result is a list of tuples
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(item, tuple) for item in result))
        self.assertTrue(all(len(item) == 2 for item in result))
        
        # Check first element is root at level 0
        self.assertEqual(result[0][0], 'root')
        self.assertEqual(result[0][1], 0)
        
        # Check that children have level > 0
        for tag, level in result[1:]:
            self.assertGreater(level, 0)
    
    def test_ldPair_single_node(self):
        """Test ldPair on a single node"""
        xml_str = '<?xml version="1.0"?><single/>'
        root = ET.fromstring(xml_str)
        visited = []
        result = ldPair(root, visited)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], ('single', 0))
    
    def test_ldPair_levels(self):
        """Test that ldPair correctly assigns levels"""
        xml_str = '''<?xml version="1.0"?>
        <root>
            <child>
                <grandchild/>
            </child>
        </root>'''
        root = ET.fromstring(xml_str)
        visited = []
        result = ldPair(root, visited)
        
        # Check level progression
        levels = [level for _, level in result]
        self.assertEqual(levels[0], 0)  # root
        self.assertGreater(levels[1], levels[0])  # child
        if len(levels) > 2:
            self.assertGreater(levels[2], levels[1])  # grandchild


class TestChangeCost(unittest.TestCase):
    """Test change_cost function"""
    
    def test_change_cost_same_labels(self):
        """Test change cost for identical labels"""
        cost = change_cost('label1', 'label1')
        self.assertEqual(cost, 0)
    
    def test_change_cost_different_labels(self):
        """Test change cost for different labels"""
        cost = change_cost('label1', 'label2')
        self.assertEqual(cost, 1)
    
    def test_change_cost_empty_labels(self):
        """Test change cost with empty strings"""
        cost1 = change_cost('', '')
        self.assertEqual(cost1, 0)
        
        cost2 = change_cost('label', '')
        self.assertEqual(cost2, 1)


class TestChawatheDistance(unittest.TestCase):
    """Test chawathe_distance function"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    
    def test_chawathe_distance_identical_trees(self):
        """Test Chawathe distance between identical trees"""
        xml1 = ET.parse(os.path.join(self.test_data_dir, 'identical_tree.xml'))
        xml2 = ET.parse(os.path.join(self.test_data_dir, 'identical_tree.xml'))
        
        distance = chawathe_distance(xml1, xml2)
        
        # Distance should be 0 for identical trees
        self.assertEqual(distance, 0)
    
    def test_chawathe_distance_different_trees(self):
        """Test Chawathe distance between different trees"""
        xml1 = ET.parse(os.path.join(self.test_data_dir, 'simple_tree1.xml'))
        xml2 = ET.parse(os.path.join(self.test_data_dir, 'simple_tree2.xml'))
        
        distance = chawathe_distance(xml1, xml2)
        
        # Distance should be positive
        self.assertGreater(distance, 0)
        
        # Check it's a valid number
        self.assertIsInstance(distance, (int, float, np.number))
    
    def test_chawathe_distance_symmetric(self):
        """Test that Chawathe distance is symmetric"""
        xml1 = ET.parse(os.path.join(self.test_data_dir, 'simple_tree1.xml'))
        xml2 = ET.parse(os.path.join(self.test_data_dir, 'simple_tree2.xml'))
        
        distance1 = chawathe_distance(xml1, xml2)
        distance2 = chawathe_distance(xml2, xml1)
        
        # Distance should be symmetric
        self.assertEqual(distance1, distance2)
    
    def test_chawathe_distance_single_node(self):
        """Test Chawathe distance with single node trees"""
        xml_str1 = '<?xml version="1.0"?><root/>'
        xml_str2 = '<?xml version="1.0"?><root/>'
        
        tree1 = ET.ElementTree(ET.fromstring(xml_str1))
        tree2 = ET.ElementTree(ET.fromstring(xml_str2))
        
        distance = chawathe_distance(tree1, tree2)
        
        # Same single node should have distance 0
        self.assertEqual(distance, 0)
    
    def test_chawathe_distance_non_negative(self):
        """Test that Chawathe distance is always non-negative"""
        xml1 = ET.parse(os.path.join(self.test_data_dir, 'simple_tree1.xml'))
        xml2 = ET.parse(os.path.join(self.test_data_dir, 'simple_tree2.xml'))
        
        distance = chawathe_distance(xml1, xml2)
        
        self.assertGreaterEqual(distance, 0)


if __name__ == '__main__':
    unittest.main()
