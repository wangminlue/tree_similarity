# tree_similarity

the main function is tree_exp() in get_XML_cluster.py

## Requirements
 
1. ZSS module is at https://pypi.python.org/pypi/zss/1.1.4

2. The java implementation of APTED is from https://github.com/DatabaseGroup/apted

   After building apted, please first apted.jar to the current directory.

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

## Testing

This project includes a comprehensive test suite with 55+ test cases covering all modules.

### Run all tests:

```bash
python -m unittest discover tests -v
```

Or use the test runner:

```bash
python tests/run_tests.py
```

### Test Coverage

The test suite covers:
- **GSSTree.py**: Graph Structure Similarity algorithm (21 tests)
- **chawatheDistance.py**: Chawathe distance algorithm (13 tests)
- **XMLDistance.py**: Zhang-Shasha distance algorithm (8 tests)
- **RTED.py**: APTED distance algorithm (7 tests)
- **get_XML_clusters.py**: Cluster operations and statistics (13 tests)

For detailed test documentation, see:
- `tests/README.md` - Test suite documentation
- `TEST_COVERAGE.md` - Comprehensive coverage report

All tests pass on Python 3.x with proper dependencies installed.

