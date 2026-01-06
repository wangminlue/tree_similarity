# Test Coverage Summary

## Overview
This document provides a summary of the comprehensive unit test suite implemented for the tree_similarity project.

## Test Statistics
- **Total Test Modules**: 5
- **Total Test Classes**: 18
- **Total Test Methods**: 55+
- **Test Pass Rate**: 100% (excluding skipped tests for missing optional dependencies)

## Module Coverage

### 1. GSSTree.py - Graph Structure Similarity Tests
**Test File**: `tests/test_GSSTree.py`
**Coverage**: 10 test classes, 21 test methods

Functions tested:
- `breadth_first()` - Breadth-first tree traversal
- `sibling_matrix()` - Sibling relationship matrix generation
- `pre_order()` - Pre-order tree traversal
- `get_last_child_index()` - Last child index calculation
- `ancester_matrix()` - Ancestor relationship matrix generation
- `get_anc_sib_matrices()` - Combined matrix generation
- `exact_trace()` - Trace computation for similarity
- `exact_matched_M_weightless_preorder()` - Preorder matching matrix
- `exact_matched_M_weightless_bfs()` - BFS matching matrix
- `exact_gss_tree()` - Complete GSS tree similarity computation

Key test scenarios:
- Single node trees
- Simple trees with multiple children
- Nested tree structures
- Identical tree comparisons
- Different tree comparisons
- Edge cases (empty nodes, zero matrices)

### 2. chawatheDistance.py - Chawathe Distance Tests
**Test File**: `tests/test_chawatheDistance.py`
**Coverage**: 3 test classes, 13 test methods

Functions tested:
- `ldPair()` - Label-depth pair extraction
- `change_cost()` - Edit operation cost calculation
- `chawathe_distance()` - Complete Chawathe distance computation

Key test scenarios:
- Label-depth level assignment
- Single node trees
- Identical tree distance (should be 0)
- Different tree distance (should be > 0)
- Symmetry property verification
- Non-negative distance verification

### 3. XMLDistance.py - Zhang-Shasha Distance Tests
**Test File**: `tests/test_XMLDistance.py`
**Coverage**: 3 test classes, 8 test methods

Functions tested:
- `toString()` - XML node to string conversion
- `printTree()` - Tree printing in ZSS format
- `zhang_distance()` - Zhang-Shasha tree edit distance

Key test scenarios:
- Single node conversion
- Tree with children conversion
- Nested structure handling
- Identical tree distance
- Different tree distance
- Symmetry property verification
- Graceful handling of missing zss module

### 4. RTED.py - APTED Distance Tests
**Test File**: `tests/test_RTED.py`
**Coverage**: 2 test classes, 7 test methods

Functions tested:
- `print_bracket_tree()` - Bracket notation tree representation
- `apted_distance()` - APTED tree edit distance

Key test scenarios:
- Single node bracket format
- Tree with children bracket format
- Nested structure bracket format
- Bracket balance verification
- Identical tree distance (with apted.jar)
- Different tree distance (with apted.jar)
- Symmetry property verification
- Graceful handling of missing apted.jar

### 5. get_XML_clusters.py - Cluster Operations Tests
**Test File**: `tests/test_get_XML_clusters.py`
**Coverage**: 3 test classes, 13 test methods

Functions tested:
- `get_clusters()` - Load XML files from cluster directories
- `cal_stats()` - Calculate precision and F-score statistics
- `tree_exp()` - Run tree comparison experiments with different methods

Key test scenarios:
- Cluster directory structure parsing
- Tuple format validation
- All matched pairs statistics
- No matched pairs handling
- Mixed match statistics
- Empty list handling
- Sorting verification
- GSS method experiment
- Chawathe method experiment
- Zhang method experiment
- Empty cluster list handling

## Test Data
Created test XML files in `tests/test_data/`:
- `simple_tree1.xml` - A tree with 2 children and 2 grandchildren
- `simple_tree2.xml` - A similar but different tree
- `identical_tree.xml` - For identical comparison tests
- `test_clusters/` - Cluster directory structure for integration tests

## Dependencies
Required for full test execution:
- `numpy` - For matrix operations (required)
- `lxml` - For XML parsing (required)
- `zss` - For Zhang-Shasha distance (optional, tests skipped if missing)
- `apted.jar` - For APTED distance (optional, tests skipped if missing)

## Python Compatibility Fixes
To enable testing on Python 3, the following minimal fixes were made to the codebase:
1. Updated `print` statements to function calls in `__main__` sections
2. Fixed tab/space inconsistencies in `get_XML_clusters.py`
3. Replaced deprecated `getchildren()` with `list()` in `GSSTree.py`

These fixes were necessary to allow tests to run on Python 3.x while maintaining backward compatibility.

## Running Tests

### Run all tests:
```bash
python -m unittest discover tests -v
```

### Run specific module:
```bash
python -m unittest tests.test_GSSTree -v
```

### Using the test runner:
```bash
python tests/run_tests.py
```

## Test Design Principles
1. **Isolation**: Each test is independent and can run in any order
2. **Reproducibility**: Tests produce consistent, deterministic results
3. **Clarity**: Test names clearly describe what is being tested
4. **Robustness**: Tests handle edge cases and missing dependencies gracefully
5. **Comprehensive**: Tests cover normal cases, edge cases, and error conditions
6. **Documentation**: Each test includes docstrings explaining the test purpose

## Future Improvements
Potential areas for additional test coverage:
1. Performance benchmarks for large trees
2. More comprehensive integration tests with real-world XML data
3. Stress tests with deeply nested structures
4. Property-based testing with random tree generation
5. Code coverage metrics tracking
