#!/usr/bin/env python3
"""
Comprehensive test runner for apply_patch script.
Runs all test patches and reports results.
"""

import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

# Test definitions: (test_name, patch_file, setup_files, expected_result)
# setup_files is a list of (source_path, dest_path) tuples to copy before test
# expected_result: True = should succeed, False = should fail

TESTS = [
    # Original basic tests
    ("basic_add", "test_add.patch", [], True),
    (
        "basic_update",
        "test_update.patch",
        [("test_update_input.txt", "test_update_input.txt")],
        True,
    ),
    ("basic_move", "test_move.patch", [("test_output.txt", "test_output.txt")], True),
    (
        "basic_delete",
        "test_delete.patch",
        [("test_output_renamed.txt", "test_output_renamed.txt")],
        True,
    ),
    ("expected_fail", "test_fail.patch", [], False),
    # Complex tests
    (
        "multiple_operations",
        "test_multiple_operations.patch",
        [
            ("test_multi/existing_file.txt", "test_multi/existing_file.txt"),
            ("test_multi/delete_me.txt", "test_multi/delete_me.txt"),
            ("test_multi/move_me.txt", "test_multi/move_me.txt"),
        ],
        True,
    ),
    (
        "multiple_chunks",
        "test_multiple_chunks.patch",
        [
            ("test_chunks.txt", "test_chunks.txt"),
        ],
        True,
    ),
    (
        "unicode_handling",
        "test_unicode.patch",
        [
            ("test_unicode.txt", "test_unicode.txt"),
        ],
        True,
    ),
    (
        "whitespace_variations",
        "test_whitespace.patch",
        [
            ("test_whitespace.txt", "test_whitespace.txt"),
        ],
        True,
    ),
    (
        "eof_anchor",
        "test_eof_anchor.patch",
        [
            ("test_eof.txt", "test_eof.txt"),
        ],
        True,
    ),
    (
        "multiline_replacement",
        "test_multiline.patch",
        [
            ("test_multiline.txt", "test_multiline.txt"),
        ],
        True,
    ),
    (
        "empty_lines",
        "test_empty_lines.patch",
        [
            ("test_empty.txt", "test_empty.txt"),
        ],
        True,
    ),
    (
        "context_variations",
        "test_context.patch",
        [
            ("test_context.txt", "test_context.txt"),
        ],
        True,
    ),
    (
        "context_reference_lines",
        "test_context_reference.patch",
        [
            ("test_context_reference.txt", "test_context_reference.txt"),
        ],
        True,
    ),
    (
        "context_reference_rename",
        "test_context_reference_rename.patch",
        [
            (
                "test_context_reference_rename.txt",
                "test_context_reference_rename.txt",
            ),
        ],
        True,
    ),
    (
        "pure_additions",
        "test_pure_additions.patch",
        [
            ("test_additions.txt", "test_additions.txt"),
        ],
        True,
    ),
    ("nested_directories", "test_nested_dirs.patch", [], True),
    (
        "deletions_only",
        "test_deletions_only.patch",
        [
            ("test_deletions.txt", "test_deletions.txt"),
        ],
        True,
    ),
    (
        "fuzzy_matching",
        "test_fuzzy_matching.patch",
        [
            ("test_fuzzy.txt", "test_fuzzy.txt"),
        ],
        True,
    ),
    (
        "large_operations",
        "test_large_operations.patch",
        [
            ("test_large/existing_large.txt", "test_large/existing_large.txt"),
            ("test_large/delete_large.txt", "test_large/delete_large.txt"),
        ],
        True,
    ),
    # Edge case tests
    (
        "heredoc_format",
        "test_heredoc.patch",
        [("test_heredoc_existing.txt", "test_heredoc_existing.txt")],
        True,
    ),
    ("special_characters", "test_special_chars.patch", [], True),
    (
        "crlf_line_endings",
        "test_crlf.patch",
        [("test_crlf.txt", "test_crlf.txt")],
        True,
    ),
    ("special_paths", "test_special_paths.patch", [], True),
    ("add_empty_file", "test_add_empty.patch", [], True),
    ("single_line_file", "test_single_line.patch", [], True),
    (
        "consecutive_updates",
        "test_consecutive_updates.patch",
        [("test_consecutive.txt", "test_consecutive.txt")],
        True,
    ),
    (
        "leading_blank_lines",
        "test_leading_blanks.patch",
        [("test_leading_blanks.txt", "test_leading_blanks.txt")],
        True,
    ),
]

EXPECTED_OUTPUTS = {
    "pure_additions": [
        ("test_additions.txt", "test_pure_additions_expected.txt"),
    ],
}


def setup_test_env(test_dir, setup_files):
    """Copy setup files to test directory."""
    script_dir = Path(__file__).parent

    for src, dst in setup_files:
        src_path = script_dir / src
        dst_path = test_dir / dst

        if src_path.exists():
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src_path, dst_path)


def run_test(_test_name, patch_file, setup_files, should_succeed, test_dir):
    """Run a single test and return result."""
    script_dir = Path(__file__).parent
    patch_path = script_dir / patch_file
    apply_patch = script_dir.parent / "scripts" / "apply_patch"
    expected_outputs = EXPECTED_OUTPUTS.get(_test_name, [])

    # Setup test files
    setup_test_env(test_dir, setup_files)

    # Run the patch
    try:
        result = subprocess.run(
            [str(apply_patch), str(patch_path)],
            cwd=test_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )

        succeeded = result.returncode == 0

        if succeeded != should_succeed:
            return (
                False,
                f"Expected {'success' if should_succeed else 'failure'}, got exit code {result.returncode}\nstdout: {result.stdout}\nstderr: {result.stderr}",
            )

        if succeeded:
            for actual_name, expected_name in expected_outputs:
                actual_path = test_dir / actual_name
                expected_path = script_dir / expected_name

                if not actual_path.exists():
                    return False, f"Expected output file missing: {actual_path}"

                actual_content = actual_path.read_text(encoding="utf-8")
                expected_content = expected_path.read_text(encoding="utf-8")
                if actual_content != expected_content:
                    return (
                        False,
                        f"Output mismatch for {actual_name}\nexpected:\n{expected_content}\nactual:\n{actual_content}",
                    )

        return True, f"Exit code: {result.returncode}"

    except subprocess.TimeoutExpired:
        return False, "Test timed out"
    except Exception as e:
        return False, f"Exception: {e}"


def main():
    print("=" * 70)
    print("apply_patch Comprehensive Test Suite")
    print("=" * 70)
    print()

    passed = 0
    failed = 0

    for test_name, patch_file, setup_files, should_succeed in TESTS:
        print(f"Running: {test_name}...", end=" ")

        with tempfile.TemporaryDirectory() as test_dir:
            success, message = run_test(
                test_name, patch_file, setup_files, should_succeed, Path(test_dir)
            )

            if success:
                print("✓ PASSED")
                passed += 1
            else:
                print("✗ FAILED")
                print(f"  {message}")
                failed += 1

    print()
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
