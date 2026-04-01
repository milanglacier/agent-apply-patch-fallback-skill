# Python Patch Tool

A Python implementation of the opencode `apply_patch` tool that applies patch files to your codebase without permission checks.

## Features

- Supports the same patch format as opencode's `apply_patch` tool
- Applies patches directly without interactive permission prompts
- Returns clear error messages when patches fail to apply
- Fuzzy matching with multiple fallback strategies
- Supports Add, Update, Delete, and Move operations

## Installation

```bash
# Copy to a directory in your PATH
cp scripts/apply_patch ~/.local/bin/
# Or use directly from scripts folder
./scripts/apply_patch patch.txt
```

## Usage

```bash
# Apply from file
apply_patch patch.txt

# Apply from stdin
cat patch.txt | apply_patch
apply_patch <<'EOF'
*** Begin Patch
*** Add File: hello.txt
+Hello, World!
*** End Patch
EOF

# Apply with specific base directory
apply_patch -d /path/to/project patch.txt

# Verbose mode
apply_patch -v patch.txt
```

## Patch Format

The patch format is a simplified, file-oriented diff:

```
*** Begin Patch
*** Add File: <path>
+<content lines>
*** Update File: <path>
*** Move to: <new_path>  (optional)
@@ <context line>
-<old line>
+<new line>
*** Delete File: <path>
*** End Patch
```

### Examples

**Add a file:**

```
*** Begin Patch
*** Add File: src/main.py
+def main():
+    print("Hello")
+
+if __name__ == "__main__":
+    main()
*** End Patch
```

**Update a file:**

```
*** Begin Patch
*** Update File: src/main.py
@@ def main():
-    print("Hello")
+    print("Hello, World!")
*** End Patch
```

**Move/Rename a file:**

```
*** Begin Patch
*** Update File: src/main.py
*** Move to: src/app.py
@@ def main():
-    print("Hello, World!")
+    print("Hi!")
*** End Patch
```

**Delete a file:**

```
*** Begin Patch
*** Delete File: src/old.py
*** End Patch
```

**Multiple operations in one patch:**

```
*** Begin Patch
*** Add File: config.json
+{"setting": true}
*** Update File: src/main.py
@@ import os
-import sys
+import json
*** Delete File: temp.txt
*** End Patch
```

## Exit Codes

- `0` - Success
- `1` - Parse error (invalid patch format)
- `2` - Application error (file not found, match failed, etc.)
- `3` - I/O error
- `130` - Interrupted (Ctrl+C)

## Error Handling

The tool provides detailed error messages:

```bash
$ apply_patch broken.patch
Apply error: Failed to find context 'def foo():' in /path/to/file.py

$ apply_patch missing.patch
Apply error: File to update not found: /path/to/missing.txt

$ apply_patch <<'EOF'
*** Begin Patch
*** End Patch
EOF
Error: patch rejected: empty patch
```

## Matching Strategy

For update operations, the tool tries to find matching text using multiple strategies:

1. **Exact match** - Exact string comparison
2. **Rstrip match** - Match with trailing whitespace ignored
3. **Trim match** - Match with all whitespace normalized
4. **Unicode normalized** - Match with Unicode punctuation normalized to ASCII

This allows patches to apply even when there are minor whitespace or encoding differences.

## Testing

Run the included test patches:

```bash
cd test

# Add
../scripts/apply_patch test_add.patch

# Update
../scripts/apply_patch test_update.patch

# Move
../scripts/apply_patch test_move.patch

# Delete
../scripts/apply_patch test_delete.patch

# Failure case
../scripts/apply_patch test_fail.patch  # Returns error code
```
