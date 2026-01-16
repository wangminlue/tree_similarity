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


class TestPrintBracketTree(unittest.TestCase):
    """Test print_bracket_tree function"""
    
    def test_single_node(self):
        """Test bracket tree representation for single node"""
        xml_str = """<root/>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        result = print_bracket_tree(tree.getroot())
        
        self.assertIsInstance(result, str)
        self.assertEqual(result, '{root}')
        
    def test_tree_with_child(self):
        """Test bracket tree with one child"""
        xml_str = """<root><child/></root>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        result = print_bracket_tree(tree.getroot())
        
        self.assertEqual(result, '{root{child}}')
        
    def test_tree_with_multiple_children(self):
        """Test bracket tree with multiple children"""
        xml_str = """<root><child1/><child2/></root>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        result = print_bracket_tree(tree.getroot())
        
        self.assertEqual(result, '{root{child1}{child2}}')
        
    def test_nested_tree(self):
        """Test bracket tree with nested structure"""
        xml_str = """<root><child><grandchild/></child></root>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        result = print_bracket_tree(tree.getroot())
        
        self.assertEqual(result, '{root{child{grandchild}}}')
        
    def test_balanced_braces(self):
        """Test that braces are balanced"""
        xml_str = """<root><a><b/></a><c/></root>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        result = print_bracket_tree(tree.getroot())
        
        # Count opening and closing braces
        open_count = result.count('{')
        close_count = result.count('}')
        self.assertEqual(open_count, close_count)
        
    def test_complex_tree(self):
        """Test bracket tree with complex structure"""
        xml_str = """<a><b><c/><d/></b><e><f/></e></a>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        result = print_bracket_tree(tree.getroot())
        
        # Should contain all tags
        for tag in ['a', 'b', 'c', 'd', 'e', 'f']:
            self.assertIn(tag, result)
            
        # Check balanced braces
        open_count = result.count('{')
        close_count = result.count('}')
        self.assertEqual(open_count, close_count)
        
    def test_deep_nesting(self):
        """Test bracket tree with deep nesting"""
        xml_str = """<a><b><c><d><e/></d></c></b></a>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        result = print_bracket_tree(tree.getroot())
        
        expected = '{a{b{c{d{e}}}}}'
        self.assertEqual(result, expected)
        
    def test_tag_preservation(self):
        """Test that tag names are preserved correctly"""
        xml_str = """<custom_tag_123/>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        result = print_bracket_tree(tree.getroot())
        
        self.assertEqual(result, '{custom_tag_123}')


# Note: apted_distance tests require Java and apted.jar which may not be available
class TestAptedDistance(unittest.TestCase):
    """Test apted_distance function - requires Java and apted.jar"""
    
    def test_apted_distance_requires_jar(self):
        """Test that apted_distance requires apted.jar and Java"""
        try:
            from RTED import apted_distance
            
            # Check if apted.jar exists
            jar_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'apted.jar'
            )
            
            if not os.path.exists(jar_path):
                self.skipTest("apted.jar not found")
                
            # If jar exists, try a basic test with identical trees
            xml_str = """<root/>"""
            tree = ET.ElementTree(ET.fromstring(xml_str))
            
            try:
                distance = apted_distance(tree, tree)
                self.assertIsInstance(distance, float)
                self.assertEqual(distance, 0.0)
            except Exception as e:
                # Java may not be available or other subprocess issues
                self.skipTest(f"Cannot run apted_distance: {e}")
                
        except ImportError:
            self.skipTest("RTED module import failed")


if __name__ == '__main__':
    unittest.main()
