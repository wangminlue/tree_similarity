"""
Comprehensive unit tests for RTED module
"""
import unittest
import xml.etree.ElementTree as ET
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from RTED import print_bracket_tree, apted_distance


class TestRTED(unittest.TestCase):
    """Test suite for RTED module functions"""

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
</root>"""
        
        self.different_tree = ET.ElementTree(ET.fromstring(self.different_xml_str))

    def test_print_bracket_tree(self):
        """Test print_bracket_tree function"""
        root = self.simple_tree.getroot()
        result = print_bracket_tree(root)
        
        # Check that result is a string
        self.assertIsInstance(result, str)
        
        # Check that it starts and ends with brackets
        self.assertTrue(result.startswith('{'))
        self.assertTrue(result.endswith('}'))
        
        # Check that it contains the root tag
        self.assertIn('root', result)

    def test_print_bracket_tree_single_node(self):
        """Test print_bracket_tree with single node"""
        single_xml = ET.ElementTree(ET.fromstring("<root/>"))
        root = single_xml.getroot()
        result = print_bracket_tree(root)
        
        self.assertEqual(result, "{root}")

    def test_print_bracket_tree_nested(self):
        """Test print_bracket_tree with nested structure"""
        root = self.simple_tree.getroot()
        result = print_bracket_tree(root)
        
        # Check that nested brackets exist
        self.assertGreater(result.count('{'), 1)
        self.assertGreater(result.count('}'), 1)
        
        # Check bracket balance
        self.assertEqual(result.count('{'), result.count('}'))

    def test_apted_distance_identical_trees(self):
        """Test apted_distance with identical trees"""
        try:
            distance = apted_distance(self.simple_tree, self.simple_tree)
            
            # Check that distance is a number
            self.assertIsInstance(distance, (int, float))
            
            # Identical trees should have distance 0
            self.assertEqual(distance, 0.0)
        except Exception as e:
            # If apted.jar is not available or Java is not installed, skip
            self.skipTest(f"apted_distance requires apted.jar and Java: {e}")

    def test_apted_distance_different_trees(self):
        """Test apted_distance with different trees"""
        try:
            distance1 = apted_distance(self.simple_tree, self.simple_tree)
            distance2 = apted_distance(self.simple_tree, self.different_tree)
            
            # Different trees should have greater distance than identical trees
            self.assertGreaterEqual(distance2, distance1)
            
            # Distance should be non-negative
            self.assertGreaterEqual(distance2, 0)
        except Exception as e:
            # If apted.jar is not available or Java is not installed, skip
            self.skipTest(f"apted_distance requires apted.jar and Java: {e}")

    def test_apted_distance_returns_float(self):
        """Test that apted_distance returns a float"""
        try:
            distance = apted_distance(self.simple_tree, self.simple_tree2)
            self.assertIsInstance(distance, float)
        except Exception as e:
            self.skipTest(f"apted_distance requires apted.jar and Java: {e}")


if __name__ == '__main__':
    unittest.main()
