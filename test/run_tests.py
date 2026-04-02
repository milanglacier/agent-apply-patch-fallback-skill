#!/usr/bin/env python3
"""
Comprehensive test runner for apply_patch script.
Runs all test patches and reports results.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TESTS = [
    ("basic_add", True),
    ("basic_update", True),
    ("basic_move", True),
    ("basic_delete", True),
    ("expected_fail", False),
    ("multiple_operations", True),
    ("multiple_chunks", True),
    ("unicode_handling", True),
    ("whitespace_variations", True),
    ("eof_anchor", True),
    ("multiline_replacement", True),
    ("empty_lines", True),
    ("context_variations", True),
    ("context_reference_lines", True),
    ("context_reference_rename", True),
    ("pure_additions", True),
    ("nested_directories", True),
    ("deletions_only", True),
    ("fuzzy_matching", True),
    ("large_operations", True),
    ("heredoc_format", True),
    ("special_characters", True),
    ("crlf_line_endings", True),
    ("special_paths", True),
    ("add_empty_file", True),
    ("single_line_file", True),
    ("consecutive_updates", True),
    ("leading_blank_lines", True),
]


def copy_tree(source_dir, dest_dir):
    """Copy a case tree into the temp directory."""
    if source_dir.exists():
        shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)


def collect_tree(root_dir):
    """Return the relative file tree and contents for a test directory."""
    tree = {}

    if not root_dir.exists():
        return tree

    for path in sorted(root_dir.rglob("*")):
        if path.is_file():
            tree[path.relative_to(root_dir).as_posix()] = path.read_text(
                encoding="utf-8"
            )

    return tree


def run_test(test_name, should_succeed, test_dir):
    """Run a single test and return result."""
    script_dir = Path(__file__).parent
    case_dir = script_dir / "cases" / test_name
    patch_path = case_dir / "patch.patch"
    before_dir = case_dir / "before"
    after_dir = case_dir / "after"
    apply_patch = script_dir.parent / "scripts" / "apply_patch"

    if not patch_path.exists():
        return False, f"Missing patch file: {patch_path}"

    if should_succeed and not after_dir.exists():
        return False, f"Successful test has no after/ tree: {after_dir}"

    if not should_succeed and after_dir.exists():
        return False, f"Failing test should not define after/: {after_dir}"

    copy_tree(before_dir, test_dir)

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
            expected_tree = collect_tree(after_dir)
            actual_tree = collect_tree(test_dir)

            if set(actual_tree) != set(expected_tree):
                missing_files = sorted(set(expected_tree) - set(actual_tree))
                extra_files = sorted(set(actual_tree) - set(expected_tree))
                return (
                    False,
                    f"File tree mismatch\nexpected files: {sorted(expected_tree)}\nactual files: {sorted(actual_tree)}\nmissing: {missing_files}\nextra: {extra_files}",
                )

            for relative_path, expected_content in expected_tree.items():
                actual_content = actual_tree[relative_path]
                if actual_content != expected_content:
                    return (
                        False,
                        f"Output mismatch for {relative_path}\nexpected:\n{expected_content!r}\nactual:\n{actual_content!r}",
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

    for test_name, should_succeed in TESTS:
        print(f"Running: {test_name}...", end=" ")

        with tempfile.TemporaryDirectory() as test_dir:
            success, message = run_test(test_name, should_succeed, Path(test_dir))

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
