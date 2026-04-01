# apply_patch Test Suite

Comprehensive test suite for the `apply_patch` Python script.

## Running Tests

```bash
# Run all tests
python3 run_tests.py

# Run individual test patches (from test directory)
../scripts/apply_patch test_add.patch
../scripts/apply_patch test_update.patch
```

## Test Coverage

### Basic Operations (5 tests)
- **basic_add** - Create new files
- **basic_update** - Modify existing file content
- **basic_move** - Rename/move files with content changes
- **basic_delete** - Delete files
- **expected_fail** - Verify proper error handling for non-existent files

### Complex Scenarios (13 tests)
- **multiple_operations** - Multiple file operations in single patch (add, update, delete, move)
- **multiple_chunks** - Multiple @@ sections updating same file
- **unicode_handling** - Unicode punctuation normalization (smart quotes, em-dash, ellipsis)
- **whitespace_variations** - Trailing spaces, tabs, mixed whitespace
- **eof_anchor** - End-of-file anchor matching
- **multiline_replacement** - Replacing multiple consecutive lines
- **empty_lines** - Handling blank lines and edge cases
- **context_variations** - Context lines with special characters and unicode
- **pure_additions** - Adding content without removing (empty old_lines)
- **nested_directories** - Creating deeply nested directory structures
- **deletions_only** - Removing lines without adding new ones
- **fuzzy_matching** - Fuzzy matching with whitespace/unicode variations
- **large_operations** - Large file updates, multiple hunks

### Edge Cases (4 tests)
- **heredoc_format** - Patch format parsing
- **special_characters** - Non-alphanumeric characters in content
- **crlf_line_endings** - Windows-style line endings
- **special_paths** - Paths with spaces and quotes

## Test Structure

Each test consists of:
- **Patch file** (`test_*.patch`) - The patch to apply
- **Input files** - Files copied to temp directory before patching
- **Expected result** - Whether the patch should succeed or fail

Tests run in isolated temporary directories to prevent interference.

## Adding New Tests

To add a new test:

1. Create a patch file: `test_mytest.patch`
2. Create any needed input files
3. Add test to `run_tests.py`:

```python
(
    "my_test_name",           # Test identifier
    "test_mytest.patch",      # Patch filename
    [("input.txt", "input.txt")],  # Files to copy (src, dest)
    True                      # Expected to succeed
),
```

## Exit Codes

Test runner returns:
- `0` - All tests passed
- `1` - One or more tests failed
