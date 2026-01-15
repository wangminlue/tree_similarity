"""
Unit tests for XMLDistance.py - Zhang-Shasha distance algorithm
"""
import unittest
import xml.etree.ElementTree as ET
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import, but skip tests if zss is not available
try:
    from XMLDistance import printTree, toString
    ZSS_AVAILABLE = True
except ImportError:
    ZSS_AVAILABLE = False


@unittest.skipIf(not ZSS_AVAILABLE, "zss module not available")
class TestXMLDistance(unittest.TestCase):
    """Test cases for XMLDistance module"""

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

    def test_toString_simple(self):
        """Test toString function"""
        root = self.simple_tree.getroot()
        result = toString(root)
        
        # Check that result is a string
        self.assertIsInstance(result, str)
        
        # Check that it contains Node and tag name
        self.assertIn('Node', result)
        self.assertIn('root', result)
        
        # Check format is correct
        self.assertTrue(result.startswith('Node("'))
        self.assertTrue(result.endswith('")'))

    def test_toString_child(self):
        """Test toString on child element"""
        root = self.simple_tree.getroot()
        child = list(root)[0]  # Get first child
        result = toString(child)
        
        self.assertIsInstance(result, str)
        self.assertIn('Node', result)
        self.assertIn('child1', result)

    def test_printTree_single_node(self):
        """Test printTree on single node"""
        root = self.single_node_tree.getroot()
        result = printTree(root)
        
        # Check that result is a string
        self.assertIsInstance(result, str)
        
        # Should start with ( and end with )
        self.assertTrue(result.startswith('('))
        self.assertTrue(result.endswith(')'))
        
        # Should contain Node("root")
        self.assertIn('Node("root")', result)

    def test_printTree_simple(self):
        """Test printTree on simple tree"""
        root = self.simple_tree.getroot()
        result = printTree(root)
        
        # Check that result is a string
        self.assertIsInstance(result, str)
        
        # Should have balanced parentheses
        self.assertEqual(result.count('('), result.count(')'))
        
        # Should contain .addkid for children
        self.assertIn('.addkid', result)
        
        # Should contain all node names
        self.assertIn('root', result)
        self.assertIn('child1', result)
        self.assertIn('child2', result)

    def test_printTree_nested_structure(self):
        """Test that printTree creates valid nested structure"""
        root = self.simple_tree.getroot()
        result = printTree(root)
        
        # Should start with (Node("root")
        self.assertTrue(result.startswith('(Node("root")'))
        
        # Each .addkid should be followed by (
        parts = result.split('.addkid')
        for part in parts[1:]:  # Skip first part before any .addkid
            self.assertTrue(part.startswith('('))

    def test_printTree_preserves_hierarchy(self):
        """Test that printTree preserves tree hierarchy"""
        # Create a tree with known structure
        xml_str = """<?xml version="1.0"?>
<a>
    <b>
        <c/>
    </b>
</a>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        root = tree.getroot()
        result = printTree(root)
        
        # Should contain all nodes
        self.assertIn('Node("a")', result)
        self.assertIn('Node("b")', result)
        self.assertIn('Node("c")', result)
        
        # b should come after a, c should come after b in the string
        pos_a = result.find('Node("a")')
        pos_b = result.find('Node("b")')
        pos_c = result.find('Node("c")')
        
        self.assertLess(pos_a, pos_b)
        self.assertLess(pos_b, pos_c)

    def test_printTree_multiple_children(self):
        """Test printTree with multiple children at same level"""
        xml_str = """<?xml version="1.0"?>
<root>
    <child1/>
    <child2/>
    <child3/>
</root>"""
        tree = ET.ElementTree(ET.fromstring(xml_str))
        root = tree.getroot()
        result = printTree(root)
        
        # Should have 3 .addkid calls for 3 children
        self.assertEqual(result.count('.addkid'), 3)
        
        # All children should be present
        self.assertIn('child1', result)
        self.assertIn('child2', result)
        self.assertIn('child3', result)

    # Note: We're not testing zhang_distance function because it uses exec()
    # and requires the zss module. Testing the helper functions provides
    # good coverage of the testable parts of this module.


if __name__ == '__main__':
    unittest.main()
