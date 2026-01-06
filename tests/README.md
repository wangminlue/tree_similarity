# Test Suite Documentation

This directory contains comprehensive unit tests for the tree_similarity project.

## Test Coverage

### test_GSSTree.py
Tests for the Graph Structure Similarity (GSS) algorithm:
- `TestBreadthFirst`: Tests breadth-first traversal
- `TestSiblingMatrix`: Tests sibling matrix generation
- `TestPreOrder`: Tests pre-order traversal
- `TestGetLastChildIndex`: Tests last child index calculation
- `TestAncesterMatrix`: Tests ancestor matrix generation
- `TestGetAncSibMatrices`: Tests combined matrix generation
- `TestExactTrace`: Tests trace computation
- `TestExactMatchedM`: Tests matching matrix generation
- `TestExactGSSTree`: Tests complete GSS tree similarity computation

### test_chawatheDistance.py
Tests for the Chawathe distance algorithm:
- `TestLdPair`: Tests label-depth pair extraction
- `TestChangeCost`: Tests change cost calculation
- `TestChawatheDistance`: Tests complete Chawathe distance computation

### test_XMLDistance.py
Tests for the Zhang-Shasha distance algorithm:
- `TestToString`: Tests XML node to string conversion
- `TestPrintTree`: Tests tree printing in ZSS format
- `TestZhangDistance`: Tests Zhang-Shasha distance computation

### test_RTED.py
Tests for the APTED (All Path Tree Edit Distance) algorithm:
- `TestPrintBracketTree`: Tests bracket tree representation
- `TestAptedDistance`: Tests APTED distance computation

### test_get_XML_clusters.py
Tests for cluster operations and statistics:
- `TestGetClusters`: Tests cluster loading from directories
- `TestCalStats`: Tests statistics calculation (precision, F-score)
- `TestTreeExp`: Tests tree comparison experiments

## Running Tests

### Run all tests:
```bash
python tests/run_tests.py
```

### Run specific test module:
```bash
python -m unittest tests.test_GSSTree
```

### Run specific test class:
```bash
python -m unittest tests.test_GSSTree.TestExactGSSTree
```

### Run specific test method:
```bash
python -m unittest tests.test_GSSTree.TestExactGSSTree.test_exact_gss_tree_identical
```

## Test Data

The `test_data/` directory contains sample XML files used for testing:
- `simple_tree1.xml`: A simple tree with multiple children
- `simple_tree2.xml`: A slightly different tree for comparison
- `identical_tree.xml`: Used for testing identical tree comparisons

## Dependencies

Some tests require external dependencies:
- `numpy`: Required for matrix operations (used by most tests)
- `lxml`: Required for XML parsing in cluster tests
- `zss`: Required for Zhang-Shasha distance tests (may be skipped if not installed)
- `apted.jar`: Required for APTED distance tests (tests will be skipped if not found)

Tests that depend on unavailable dependencies will be skipped automatically.

## Test Design

All tests follow these principles:
- **Independence**: Each test can run independently
- **Reproducibility**: Tests produce consistent results
- **Clarity**: Test names clearly indicate what is being tested
- **Robustness**: Tests handle edge cases and missing dependencies gracefully
- **Coverage**: Tests cover normal cases, edge cases, and error conditions
