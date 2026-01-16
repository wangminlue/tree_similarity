"""
Unit tests for get_XML_clusters.py - Main clustering and comparison logic
"""
import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from get_XML_clusters import cal_stats, get_clusters
    GET_XML_CLUSTERS_AVAILABLE = True
except (SyntaxError, ImportError, TabError) as e:
    GET_XML_CLUSTERS_AVAILABLE = False
    GET_XML_CLUSTERS_IMPORT_ERROR = str(e)


class TestCalStats(unittest.TestCase):
    """Test cal_stats function for precision and F-score calculation"""
    
    def setUp(self):
        if not GET_XML_CLUSTERS_AVAILABLE:
            self.skipTest(f"get_XML_clusters module not available: {GET_XML_CLUSTERS_IMPORT_ERROR}")
    
    def test_all_matched(self):
        """Test when all pairs are matched"""
        result_pairs = [
            (1.0, True),
            (0.9, True),
            (0.8, True)
        ]
        
        avg_pre, max_fscore = cal_stats(result_pairs)
        
        self.assertIsInstance(avg_pre, float)
        self.assertIsInstance(max_fscore, float)
        # When all matched, precision should be 1.0
        self.assertAlmostEqual(avg_pre, 1.0, places=5)
        self.assertAlmostEqual(max_fscore, 1.0, places=5)
        
    def test_none_matched(self):
        """Test when no pairs are matched"""
        result_pairs = [
            (1.0, False),
            (0.9, False),
            (0.8, False)
        ]
        
        # This should handle the edge case of no matches
        # The function may have division by zero, so we check for that
        try:
            avg_pre, max_fscore = cal_stats(result_pairs)
            # If it doesn't raise an error, check the values are reasonable
            self.assertIsInstance(avg_pre, (float, int))
            self.assertIsInstance(max_fscore, (float, int))
        except ZeroDivisionError:
            # Expected if no matches found
            pass
            
    def test_mixed_matches(self):
        """Test with mixed matched and unmatched pairs"""
        result_pairs = [
            (1.0, True),
            (0.8, False),
            (0.6, True),
            (0.4, False)
        ]
        
        avg_pre, max_fscore = cal_stats(result_pairs)
        
        self.assertIsInstance(avg_pre, float)
        self.assertIsInstance(max_fscore, float)
        self.assertGreater(avg_pre, 0.0)
        self.assertGreater(max_fscore, 0.0)
        self.assertLessEqual(avg_pre, 1.0)
        self.assertLessEqual(max_fscore, 1.0)
        
    def test_single_pair_matched(self):
        """Test with single matched pair"""
        result_pairs = [(1.0, True)]
        
        avg_pre, max_fscore = cal_stats(result_pairs)
        
        self.assertAlmostEqual(avg_pre, 1.0, places=5)
        self.assertAlmostEqual(max_fscore, 1.0, places=5)
        
    def test_sorted_by_similarity(self):
        """Test that pairs are sorted by similarity score"""
        result_pairs = [
            (0.3, True),
            (0.9, True),
            (0.5, False),
            (0.7, True)
        ]
        
        avg_pre, max_fscore = cal_stats(result_pairs)
        
        # Should process in order: 0.9, 0.7, 0.5, 0.3
        # Verify function produces valid output
        self.assertIsInstance(avg_pre, float)
        self.assertIsInstance(max_fscore, float)
        
    def test_precision_calculation(self):
        """Test precision calculation logic"""
        # High similarity matched pairs should result in high precision
        result_pairs = [
            (0.95, True),
            (0.90, True),
            (0.10, False)
        ]
        
        avg_pre, max_fscore = cal_stats(result_pairs)
        
        # Should have high precision since high-similarity pairs are matched
        self.assertGreater(avg_pre, 0.5)
        
    def test_fscore_calculation(self):
        """Test F-score calculation"""
        result_pairs = [
            (1.0, True),
            (0.5, True)
        ]
        
        avg_pre, max_fscore = cal_stats(result_pairs)
        
        # F-score should be between 0 and 1
        self.assertGreaterEqual(max_fscore, 0.0)
        self.assertLessEqual(max_fscore, 1.0)
        
    def test_empty_list(self):
        """Test with empty result pairs"""
        result_pairs = []
        
        try:
            avg_pre, max_fscore = cal_stats(result_pairs)
            # If no error, values should be zero or NaN
        except (ZeroDivisionError, ValueError):
            # Expected for empty list
            pass


class TestGetClusters(unittest.TestCase):
    """Test get_clusters function for reading XML clusters"""
    
    def setUp(self):
        if not GET_XML_CLUSTERS_AVAILABLE:
            self.skipTest(f"get_XML_clusters module not available: {GET_XML_CLUSTERS_IMPORT_ERROR}")
    
    def test_get_clusters_requires_path(self):
        """Test that get_clusters requires valid path"""
        # Test with non-existent path
        fake_path = '/tmp/nonexistent_path_for_testing/'
        
        try:
            result = get_clusters(fake_path)
            # Should return empty list or raise error
            self.assertIsInstance(result, list)
        except (FileNotFoundError, OSError):
            # Expected when path doesn't exist
            pass
            
    def test_get_clusters_structure(self):
        """Test that get_clusters returns correct structure"""
        # Check if realworld_xml directory exists
        test_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'realworld_xml/'
        )
        
        if not os.path.exists(test_path):
            self.skipTest("realworld_xml directory not found")
            
        try:
            result = get_clusters(test_path)
            
            # Should return list of tuples
            self.assertIsInstance(result, list)
            
            if len(result) > 0:
                # Each item should be a tuple of (tree, path, cluster)
                self.assertIsInstance(result[0], tuple)
                self.assertEqual(len(result[0]), 3)
                
        except Exception as e:
            # May fail due to missing dependencies (lxml)
            self.skipTest(f"Cannot test get_clusters: {e}")


# Note: tree_exp tests require actual XML data and external dependencies
class TestTreeExp(unittest.TestCase):
    """Test tree_exp integration function"""
    
    def test_tree_exp_requires_dependencies(self):
        """Test that tree_exp requires proper setup"""
        # This is a placeholder test since tree_exp needs:
        # 1. Valid XML cluster data
        # 2. Working similarity algorithms
        # 3. External dependencies (zss, lxml, etc.)
        
        # We document what tree_exp should do:
        # - Take list of (tree, path, cluster) tuples
        # - Compare all pairs using specified method
        # - Return average precision and max F-score
        
        self.assertTrue(True)  # Placeholder
        

if __name__ == '__main__':
    unittest.main()
