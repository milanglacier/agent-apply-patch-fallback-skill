---
name: apply-patch-fallback
description: Use this skill when you need to edit files but the environment has no native apply_patch or file edit tools available. This provides a shell-based fallback using the apply_patch Python script. The skill is designed for agents running in constrained environments (remote shells, minimal containers, CI/CD pipelines) where you can execute shell commands but lack built-in file editing capabilities.
---

# Apply Patch Fallback

Use the `apply_patch` Python script to edit files when no native file editing tools are available.

## When to Use This Skill

- The environment has no built-in `apply_patch`, `edit`, or `write` tools
- You're working via SSH or in a minimal shell environment
- You can execute Python/shell commands but cannot directly modify files through API calls

## Installation

The `apply_patch` script must be available in your PATH or in the current directory:

```bash
cp scripts/apply_patch /usr/local/bin/
chmod +x /usr/local/bin/apply_patch
```

Or use it directly from the scripts folder:

```bash
./scripts/apply_patch patch.txt
```

## Patch Format

Your patch language is a stripped‑down, file‑oriented diff format:

```
*** Begin Patch
[ one or more file sections ]
*** End Patch
```

**Operations:**

- `*** Add File: <path>` — Create a new file. Every following line is prefixed with `+`.
- `*** Delete File: <path>` — Remove an existing file. Nothing follows.
- `*** Update File: <path>` — Patch an existing file in place. Optionally add `*** Move to: <new_path>` to rename.

**Update chunks use context markers:**

```
@@ <context line for positioning>
-<old line to remove>
+<new line to add>
```

## Usage

### From a file

```bash
apply_patch changes.patch
```

### Via stdin/heredoc

```bash
apply_patch <<'EOF'
*** Begin Patch
*** Add File: config.yaml
+database:
+  host: localhost
+  port: 5432
*** Update File: main.py
@@ def connect():
-    return None
+    return create_connection()
*** End Patch
EOF
```

## Example: Add a File

```bash
apply_patch <<'EOF'
*** Begin Patch
*** Add File: requirements.txt
+requests>=2.28.0
+pytest>=7.0.0
*** End Patch
EOF
```

## Example: Update a File

```bash
apply_patch <<'EOF'
*** Begin Patch
*** Update File: app.py
@@ def hello():
-    print("Hi")
+    print("Hello, World!")
*** End Patch
EOF
```

## Example: Move/Rename a File

```bash
apply_patch <<'EOF'
*** Begin Patch
*** Update File: old_name.py
*** Move to: new_name.py
@@ # Old file
+# New file location
*** End Patch
EOF
```

## Example: Delete a File

```bash
apply_patch <<'EOF'
*** Begin Patch
*** Delete File: temp.txt
*** End Patch
EOF
```

## Important Rules

1. **Always include the header** (`Add File`, `Delete File`, or `Update File`)
2. **Prefix new content lines with `+`** even when creating new files
3. **Use `@@` context lines** in updates to help locate where changes go
4. **Multiple operations** can be combined in one patch

## Error Handling

If the patch fails:

- Exit code 1: Parse error (invalid format)
- Exit code 2: Application error (file not found, lines not matched)
- Exit code 3: I/O error

The script outputs clear error messages. For match failures, verify the exact text including whitespace.

## Workflow

1. Check if native file editing tools exist — use them if available
2. If not, ensure `apply_patch` is available or download it
3. Construct your patch with proper headers
4. Apply via shell command
5. Verify the changes succeeded

## References

- Full documentation: See `references/README.md`
- Test patches: See `test/` directory for examples
