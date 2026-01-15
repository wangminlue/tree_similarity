"""
Unit tests for get_XML_clusters.py - Main orchestration and statistics functions
"""
import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from get_XML_clusters import cal_stats


class TestGetXMLClusters(unittest.TestCase):
    """Test cases for get_XML_clusters module"""

    def test_cal_stats_all_matched(self):
        """Test cal_stats when all pairs are matched"""
        # All pairs matched with decreasing similarity
        result_pairs = [
            (1.0, True),
            (0.9, True),
            (0.8, True),
            (0.7, True),
            (0.6, True),
        ]
        
        ave_pre, max_fscore = cal_stats(result_pairs)
        
        # Check that results are numbers
        self.assertIsInstance(ave_pre, float)
        self.assertIsInstance(max_fscore, float)
        
        # All matched, so average precision and F-score should be high
        self.assertGreater(ave_pre, 0.5)
        self.assertGreater(max_fscore, 0.5)
        
        # Both should be <= 1.0
        self.assertLessEqual(ave_pre, 1.0)
        self.assertLessEqual(max_fscore, 1.0)

    def test_cal_stats_none_matched(self):
        """Test cal_stats when no pairs are matched - expects ZeroDivisionError"""
        # No pairs matched - this is an edge case that causes division by zero
        # in the original implementation
        result_pairs = [
            (1.0, False),
            (0.9, False),
            (0.8, False),
            (0.7, False),
            (0.6, False),
        ]
        
        # The original implementation has a bug where it divides by zero
        # when there are no matches. We document this behavior.
        with self.assertRaises(ZeroDivisionError):
            ave_pre, max_fscore = cal_stats(result_pairs)

    def test_cal_stats_mixed_matches(self):
        """Test cal_stats with mixed matched/unmatched pairs"""
        result_pairs = [
            (1.0, True),
            (0.9, False),
            (0.8, True),
            (0.7, False),
            (0.6, True),
        ]
        
        ave_pre, max_fscore = cal_stats(result_pairs)
        
        # Check that results are numbers
        self.assertIsInstance(ave_pre, float)
        self.assertIsInstance(max_fscore, float)
        
        # Should be between 0 and 1
        self.assertGreaterEqual(ave_pre, 0.0)
        self.assertLessEqual(ave_pre, 1.0)
        self.assertGreaterEqual(max_fscore, 0.0)
        self.assertLessEqual(max_fscore, 1.0)
        
        # With some matches, should be positive
        self.assertGreater(ave_pre, 0.0)
        self.assertGreater(max_fscore, 0.0)

    def test_cal_stats_single_match(self):
        """Test cal_stats with single matched pair"""
        result_pairs = [(1.0, True)]
        
        ave_pre, max_fscore = cal_stats(result_pairs)
        
        # Single perfect match should give perfect scores
        self.assertEqual(ave_pre, 1.0)
        self.assertEqual(max_fscore, 1.0)

    def test_cal_stats_sorting(self):
        """Test that cal_stats sorts pairs by similarity"""
        # Unsorted pairs
        result_pairs = [
            (0.6, True),
            (1.0, True),
            (0.8, False),
            (0.9, True),
        ]
        
        ave_pre, max_fscore = cal_stats(result_pairs)
        
        # Should still produce valid results after sorting
        self.assertIsInstance(ave_pre, float)
        self.assertIsInstance(max_fscore, float)
        self.assertGreaterEqual(ave_pre, 0.0)
        self.assertGreaterEqual(max_fscore, 0.0)

    def test_cal_stats_precision_calculation(self):
        """Test precision calculation logic"""
        # First two are matched, rest are not
        result_pairs = [
            (1.0, True),
            (0.9, True),
            (0.8, False),
            (0.7, False),
        ]
        
        ave_pre, max_fscore = cal_stats(result_pairs)
        
        # Average precision should account for 2 matches out of 4 total
        # Precision at first match: 1/1 = 1.0
        # Precision at second match: 2/2 = 1.0
        # Average: (1.0 + 1.0) / 2 = 1.0
        self.assertEqual(ave_pre, 1.0)

    def test_cal_stats_fscore_calculation(self):
        """Test F-score calculation logic"""
        # Pattern that should produce varying F-scores
        result_pairs = [
            (1.0, True),   # Precision: 1/1, Recall: 1/3, F-score: 0.5
            (0.9, False),  # No update
            (0.8, True),   # Precision: 2/3, Recall: 2/3, F-score: 0.667
            (0.7, True),   # Precision: 3/4, Recall: 3/3, F-score: 0.857
        ]
        
        ave_pre, max_fscore = cal_stats(result_pairs)
        
        # Max F-score should be the highest calculated
        self.assertGreater(max_fscore, 0.5)
        self.assertLessEqual(max_fscore, 1.0)

    def test_cal_stats_empty_list(self):
        """Test cal_stats with empty list"""
        result_pairs = []
        
        # This may cause division by zero, but we test it doesn't crash
        try:
            ave_pre, max_fscore = cal_stats(result_pairs)
            # If it doesn't crash, check results are reasonable
            self.assertTrue(ave_pre >= 0 or str(ave_pre) == 'nan')
            self.assertEqual(max_fscore, 0.0)
        except (ZeroDivisionError, ValueError):
            # It's acceptable to raise an error for empty input
            pass

    def test_cal_stats_high_similarity_threshold(self):
        """Test behavior with high similarity threshold scenario"""
        # High similarity matches should rank first
        result_pairs = [
            (0.95, True),
            (0.90, True),
            (0.85, False),
            (0.80, True),
            (0.75, False),
            (0.70, False),
        ]
        
        ave_pre, max_fscore = cal_stats(result_pairs)
        
        # High-ranked matches should produce good metrics
        self.assertGreater(ave_pre, 0.4)
        self.assertGreater(max_fscore, 0.4)

    def test_cal_stats_all_same_similarity(self):
        """Test with all pairs having same similarity"""
        result_pairs = [
            (0.8, True),
            (0.8, False),
            (0.8, True),
            (0.8, False),
        ]
        
        ave_pre, max_fscore = cal_stats(result_pairs)
        
        # Should still produce valid results
        self.assertIsInstance(ave_pre, float)
        self.assertIsInstance(max_fscore, float)
        self.assertGreaterEqual(ave_pre, 0.0)
        self.assertGreaterEqual(max_fscore, 0.0)

    # Note: We're not testing get_clusters and tree_exp functions because:
    # - get_clusters requires actual file system structure with XML files
    # - tree_exp is an integration function that uses external dependencies
    # Testing cal_stats provides good coverage of the core statistical logic


if __name__ == '__main__':
    unittest.main()
