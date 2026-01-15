"""
Unit tests for RTED.py - APTED distance algorithm
"""
import unittest
import xml.etree.ElementTree as ET
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from RTED import print_bracket_tree


class TestRTED(unittest.TestCase):
    """Test cases for RTED module"""

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
        
        self.simple_tree = ET.ElementTree(ET.fromstring(self.simple_xml_str))
        
        # Single node tree
        self.single_node_str = """<?xml version="1.0"?>
<root/>"""
        self.single_node_tree = ET.ElementTree(ET.fromstring(self.single_node_str))

    def test_print_bracket_tree_single_node(self):
        """Test print_bracket_tree on single node"""
        root = self.single_node_tree.getroot()
        result = print_bracket_tree(root)
        
        # Check that result is a string
        self.assertIsInstance(result, str)
        
        # Should start with { and end with }
        self.assertTrue(result.startswith('{'))
        self.assertTrue(result.endswith('}'))
        
        # Should contain root tag
        self.assertIn('root', result)
        
        # For single node, should be {root}
        self.assertEqual(result, '{root}')

    def test_print_bracket_tree_simple(self):
        """Test print_bracket_tree on simple tree"""
        root = self.simple_tree.getroot()
        result = print_bracket_tree(root)
        
        # Check that result is a string
        self.assertIsInstance(result, str)
        
        # Should have balanced braces
        self.assertEqual(result.count('{'), result.count('}'))
        
        # Should contain all node tags
        self.assertIn('root', result)
        self.assertIn('child1', result)
        self.assertIn('child2', result)
        self.assertIn('grandchild1', result)

    def test_print_bracket_tree_starts_with_root(self):
        """Test that bracket tree starts with root tag"""
        root = self.simple_tree.getroot()
        result = print_bracket_tree(root)
        
        # Should start with {root
        self.assertTrue(result.startswith('{root'))

    def test_print_bracket_tree_nested_structure(self):
        """Test nested structure of bracket tree"""
        # Create a simple nested tree
        xml_str = """<?xml version="1.0"?>
<a>
    <b>
        <c/>
    </b>
</a>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        root = tree.getroot()
        result = print_bracket_tree(root)
        
        # Should contain all nodes
        self.assertIn('a', result)
        self.assertIn('b', result)
        self.assertIn('c', result)
        
        # Should have proper nesting
        # Format should be {a{b{c}}}
        self.assertTrue(result.startswith('{a'))
        self.assertTrue(result.endswith('}'))
        
        # Count braces - 3 levels should give 3 opening and 3 closing
        self.assertEqual(result.count('{'), 3)
        self.assertEqual(result.count('}'), 3)

    def test_print_bracket_tree_multiple_children(self):
        """Test bracket tree with multiple children"""
        xml_str = """<?xml version="1.0"?>
<root>
    <child1/>
    <child2/>
    <child3/>
</root>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        root = tree.getroot()
        result = print_bracket_tree(root)
        
        # All children should be present
        self.assertIn('child1', result)
        self.assertIn('child2', result)
        self.assertIn('child3', result)
        
        # Should have 4 opening braces (root + 3 children)
        self.assertEqual(result.count('{'), 4)
        self.assertEqual(result.count('}'), 4)

    def test_print_bracket_tree_preserves_order(self):
        """Test that bracket tree preserves child order"""
        xml_str = """<?xml version="1.0"?>
<root>
    <a/>
    <b/>
    <c/>
</root>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        root = tree.getroot()
        result = print_bracket_tree(root)
        
        # Children should appear in order
        pos_a = result.find('a')
        pos_b = result.find('b')
        pos_c = result.find('c')
        
        self.assertLess(pos_a, pos_b)
        self.assertLess(pos_b, pos_c)

    def test_print_bracket_tree_deep_nesting(self):
        """Test bracket tree with deep nesting"""
        xml_str = """<?xml version="1.0"?>
<a>
    <b>
        <c>
            <d>
                <e/>
            </d>
        </c>
    </b>
</a>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        root = tree.getroot()
        result = print_bracket_tree(root)
        
        # Should have 5 levels
        self.assertEqual(result.count('{'), 5)
        self.assertEqual(result.count('}'), 5)
        
        # All nodes should be present
        for tag in ['a', 'b', 'c', 'd', 'e']:
            self.assertIn(tag, result)

    # Note: We're not testing apted_distance function because it requires
    # the Java APTED library (apted.jar) to be present. Testing print_bracket_tree
    # provides good coverage of the testable parts of this module.


if __name__ == '__main__':
    unittest.main()
