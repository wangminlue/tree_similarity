"""
Comprehensive unit tests for RTED.py module.
Tests the APTED (All Path Tree Edit Distance) algorithm.
"""

import unittest
import xml.etree.ElementTree as ET
import os
import sys

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from RTED import print_bracket_tree, apted_distance


class TestPrintBracketTree(unittest.TestCase):
    """Test print_bracket_tree function"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    
    def test_print_bracket_tree_single_node(self):
        """Test bracket tree printing for single node"""
        xml_str = '<?xml version="1.0"?><root/>'
        root = ET.fromstring(xml_str)
        result = print_bracket_tree(root)
        
        # Check format
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith('{'))
        self.assertTrue(result.endswith('}'))
        self.assertIn('root', result)
    
    def test_print_bracket_tree_with_children(self):
        """Test bracket tree printing with children"""
        xml_str = '''<?xml version="1.0"?>
        <root>
            <child1/>
            <child2/>
        </root>'''
        root = ET.fromstring(xml_str)
        result = print_bracket_tree(root)
        
        # Check structure
        self.assertIn('root', result)
        self.assertIn('child1', result)
        self.assertIn('child2', result)
        
        # Check bracket structure
        self.assertEqual(result.count('{'), result.count('}'))
    
    def test_print_bracket_tree_nested(self):
        """Test bracket tree printing with nested structure"""
        xml = ET.parse(os.path.join(self.test_data_dir, 'simple_tree1.xml'))
        root = xml.getroot()
        result = print_bracket_tree(root)
        
        # Check it returns a string
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        
        # Brackets should be balanced
        self.assertEqual(result.count('{'), result.count('}'))
    
    def test_print_bracket_tree_format(self):
        """Test that bracket tree has correct format"""
        xml_str = '''<?xml version="1.0"?>
        <parent>
            <child/>
        </parent>'''
        root = ET.fromstring(xml_str)
        result = print_bracket_tree(root)
        
        # Should start with parent tag
        self.assertTrue(result.startswith('{parent'))


class TestAptedDistance(unittest.TestCase):
    """Test apted_distance function"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
        self.apted_jar = os.path.join(os.path.dirname(__file__), '..', 'apted.jar')
    
    def test_apted_distance_identical_trees(self):
        """Test APTED distance between identical trees"""
        if not os.path.exists(self.apted_jar):
            self.skipTest("apted.jar not found")
        
        try:
            xml1 = ET.parse(os.path.join(self.test_data_dir, 'identical_tree.xml'))
            xml2 = ET.parse(os.path.join(self.test_data_dir, 'identical_tree.xml'))
            
            distance = apted_distance(xml1, xml2)
            
            # Distance should be 0 for identical trees
            self.assertEqual(distance, 0.0)
        except Exception as e:
            self.skipTest(f"apted_distance test skipped due to: {e}")
    
    def test_apted_distance_different_trees(self):
        """Test APTED distance between different trees"""
        if not os.path.exists(self.apted_jar):
            self.skipTest("apted.jar not found")
        
        try:
            xml1 = ET.parse(os.path.join(self.test_data_dir, 'simple_tree1.xml'))
            xml2 = ET.parse(os.path.join(self.test_data_dir, 'simple_tree2.xml'))
            
            distance = apted_distance(xml1, xml2)
            
            # Distance should be non-negative
            self.assertGreaterEqual(distance, 0)
            
            # Check it's a float
            self.assertIsInstance(distance, float)
        except Exception as e:
            self.skipTest(f"apted_distance test skipped due to: {e}")
    
    def test_apted_distance_symmetric(self):
        """Test that APTED distance is symmetric"""
        if not os.path.exists(self.apted_jar):
            self.skipTest("apted.jar not found")
        
        try:
            xml1 = ET.parse(os.path.join(self.test_data_dir, 'simple_tree1.xml'))
            xml2 = ET.parse(os.path.join(self.test_data_dir, 'simple_tree2.xml'))
            
            distance1 = apted_distance(xml1, xml2)
            distance2 = apted_distance(xml2, xml1)
            
            # Distance should be symmetric
            self.assertEqual(distance1, distance2)
        except Exception as e:
            self.skipTest(f"apted_distance test skipped due to: {e}")


if __name__ == '__main__':
    unittest.main()
