# apply_patch Test Suite

Comprehensive test suite for the `apply_patch` Python script.

## Running Tests

```bash
# Run all tests
python3 run_tests.py

# Run an individual case patch (from test directory)
../scripts/apply_patch cases/basic_add/patch.patch
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
- **context_reference_lines** - `@@` anchor line plus additional space-prefixed reference lines
- **context_reference_rename** - `@@` anchor line plus reference lines in a renamed file
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
- **Case directory** (`cases/<name>/`) - One directory per test case
- **`patch.patch`** - The patch to apply
- **`before/`** - Optional starting tree copied into a temp directory before patching
- **`after/`** - Required for successful tests; the exact expected output tree after patching

Tests run in isolated temporary directories to prevent interference.

## Adding New Tests

To add a new test:

1. Create a case directory: `cases/my_test_name/`
2. Add `patch.patch`
3. Add `before/` if the patch needs existing files
4. Add `after/` for successful tests
5. Register the case in `run_tests.py`:

```python
("my_test_name", True),
```

## Exit Codes

Test runner returns:
- `0` - All tests passed
- `1` - One or more tests failed
