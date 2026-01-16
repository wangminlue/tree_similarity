#!/usr/bin/env python
"""
Test runner for tree_similarity unit tests

Run all tests with:
    python run_tests.py

Run specific test module:
    python run_tests.py test_gsstree
    
Run with verbose output:
    python run_tests.py -v
"""
import sys
import os
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_tests(test_module=None, verbosity=2):
    """Run unit tests"""
    
    if test_module:
        # Run specific test module
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromName(f'tests.{test_module}')
    else:
        # Discover and run all tests
        loader = unittest.TestLoader()
        start_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')
        suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    # Return 0 if successful, 1 if there were failures
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    # Parse command line arguments
    verbosity = 2
    test_module = None
    
    for arg in sys.argv[1:]:
        if arg == '-v':
            verbosity = 2
        elif arg == '-vv':
            verbosity = 3
        elif arg == '-q':
            verbosity = 1
        elif not arg.startswith('-'):
            test_module = arg
    
    sys.exit(run_tests(test_module, verbosity))
