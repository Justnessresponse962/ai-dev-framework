#!/usr/bin/env python3
"""
Prepare module structure before implementation.

Usage: python scripts/prepare_module.py <module_name> [--path=src/modules/module] [--lang=py|ts|both] [--force]

Creates: directory structure, CLAUDE.md stub, handoffs dir, test stubs
with REAL FAILING tests (NotImplementedError / throw Error) that force
the agent to implement them.
"""

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare module structure")
    parser.add_argument("module_name", help="Name of the module")
    parser.add_argument("--path", type=str, default=None,
                        help="Custom module path (default: src/modules/{name})")
    parser.add_argument("--lang", choices=["py", "ts", "both"], default=None,
                        help="Language for test stubs. If omitted, auto-detected from project files")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing module (DANGEROUS)")
    args = parser.parse_args()

    module = args.module_name
    project_root = Path(__file__).resolve().parent.parent

    module_path = args.path if args.path else f"src/modules/{module}"
    full_path = project_root / module_path

    # -- Check if module already exists ----------------------------------------
    if full_path.exists() and not args.force:
        print(f"ERROR: Module '{module}' already exists at {full_path}")
        print("Use --force to overwrite (DANGEROUS)")
        sys.exit(1)
    if full_path.exists() and args.force:
        print(f"[WARN] --force passed. Overwriting existing module at {full_path}")
    spec_file = project_root / "docs" / "specs" / f"spec_{module}.md"
    handoff_dir = project_root / "docs" / "handoffs" / module
    test_dir = full_path / "tests"

    print(f"Preparing module: {module}")
    print(f"Path: {module_path}")

    # -- Create directories --------------------------------------------------
    full_path.mkdir(parents=True, exist_ok=True)
    handoff_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)
    print("[OK] Directories created")

    # -- Create module CLAUDE.md ---------------------------------------------
    claude_md = full_path / "CLAUDE.md"
    if not claude_md.exists():
        claude_md.write_text(
            f"""# Module: {module}
# Spec: docs/specs/spec_{module}.md

## Files
| File | Lines | What it does |
|------|-------|-------------|
| --- | --- | --- |

## Dependencies
- Uses: [module X] (for what)
- Used by: [module Y] (for what)

## Key functions
- [function()] --- [what it does]

## Known issues
- [none yet]
""",
            encoding="utf-8",
        )
        print("[OK] Module CLAUDE.md created")

    # -- Create test stubs from spec -----------------------------------------
    if not spec_file.exists():
        print(f"[WARN] No spec found at {spec_file.relative_to(project_root)} -- skipping test stub generation")
        print("  Create spec first, then re-run this script")
    else:
        # Determine language: explicit --lang wins, otherwise auto-detect
        if args.lang:
            lang = args.lang
        else:
            pkg_json = project_root / "package.json"
            has_js = pkg_json.exists()
            has_py = (project_root / "requirements.txt").exists() or (project_root / "pyproject.toml").exists()
            if has_js and not has_py:
                lang = "ts"
            elif has_py and not has_js:
                lang = "py"
            elif has_js and has_py:
                print("[WARN] Mixed-stack detected (package.json + pyproject.toml/requirements.txt)")
                print("  Use --lang=py|ts|both to specify explicitly. Defaulting to 'both'.")
                lang = "both"
            else:
                lang = "py"  # no config files at all, default to Python

        if lang in ("ts", "both"):
            # TypeScript project
            test_file = test_dir / f"{module}.test.ts"
            if not test_file.exists():
                # Capitalize first letter for describe block
                describe_name = module[0].upper() + module[1:] if module else module
                test_file.write_text(
                    f"""/**
 * Test stubs for module: {module}
 * Generated from: docs/specs/spec_{module}.md
 *
 * These are FAILING stubs. The implementation agent must:
 * 1. Read the spec
 * 2. Implement each test
 * 3. Make all tests pass (TDD)
 */

describe('{describe_name}', () => {{
  // Main path tests (from User Stories)
  test('should handle main success scenario', () => {{
    throw new Error('Implement from spec: main success scenario');
  }});

  // Edge case tests (from Edge Cases section)
  test('should handle empty input', () => {{
    throw new Error('Implement from spec: empty input edge case');
  }});

  test('should handle invalid input', () => {{
    throw new Error('Implement from spec: invalid input edge case');
  }});

  test('should handle API timeout', () => {{
    throw new Error('Implement from spec: API timeout edge case');
  }});

  // Review these stubs and replace with concrete tests from the spec
}});
""",
                    encoding="utf-8",
                )
                print(f"[OK] Test stubs created (TypeScript): {test_file.relative_to(project_root)}")

            # Frontend UI test stubs
            frontend_test_dir = project_root / "tests"
            frontend_test_dir.mkdir(parents=True, exist_ok=True)
            frontend_test_file = frontend_test_dir / f"test_{module}_ui.test.ts"
            if not frontend_test_file.exists():
                frontend_test_file.write_text(
                    f"""import {{ describe, it, expect }} from 'vitest';

describe('{module} - UI Components', () => {{
  it('should render {module} list in loading state', () => {{
    throw new Error('Implement from spec: verify loading spinner/skeleton is shown');
  }});

  it('should render {module} list in empty state', () => {{
    throw new Error('Implement from spec: verify empty state message is shown');
  }});

  it('should render {module} list with data', () => {{
    throw new Error('Implement from spec: verify items are rendered correctly');
  }});

  it('should render {module} list in error state', () => {{
    throw new Error('Implement from spec: verify error message is shown');
  }});

  it('should handle {module} form submission', () => {{
    throw new Error('Implement from spec: verify form submit flow');
  }});

  it('should validate {module} form inputs', () => {{
    throw new Error('Implement from spec: verify client-side validation');
  }});
}});
""",
                    encoding="utf-8",
                )
                print(f"[OK] Frontend test stubs created: {frontend_test_file.relative_to(project_root)}")

        if lang in ("py", "both"):
            # Python project
            test_file = test_dir / f"test_{module}.py"
            if not test_file.exists():
                class_name = module.replace("_", " ").title().replace(" ", "")
                test_file.write_text(
                    f'''"""
Test stubs for module: {module}
Generated from: docs/specs/spec_{module}.md

These are FAILING stubs. The implementation agent must:
1. Read the spec
2. Implement each test
3. Make all tests pass (TDD)
"""


class Test{class_name}:
    """Main path tests (from User Stories)"""

    def test_main_success_scenario(self):
        """Implement from spec: main success scenario"""
        raise NotImplementedError("Implement from spec: main success scenario")

    def test_edge_case_empty_input(self):
        """Implement from spec: empty input edge case"""
        raise NotImplementedError("Implement from spec: empty input edge case")

    def test_edge_case_invalid_input(self):
        """Implement from spec: invalid input edge case"""
        raise NotImplementedError("Implement from spec: invalid input edge case")

    def test_edge_case_api_timeout(self):
        """Implement from spec: API timeout edge case"""
        raise NotImplementedError("Implement from spec: API timeout edge case")

    # Review these stubs and replace with concrete tests from the spec
''',
                    encoding="utf-8",
                )
                print(f"[OK] Test stubs created (Python): {test_file.relative_to(project_root)}")

    # -- Summary -------------------------------------------------------------
    print()
    print(f"Module {module} prepared:")
    print(f"  {module_path}/")
    print(f"  {module_path}/tests/")
    print(f"  {module_path}/CLAUDE.md")
    print(f"  docs/handoffs/{module}/")
    if spec_file.exists():
        test_name = f"{module}.test.ts" if (project_root / "package.json").exists() else f"test_{module}.py"
        print(f"  {module_path}/tests/{test_name}")
    print()
    print("Next: implement module using the pipeline")
    print("  database-architect -> backend-engineer -> frontend-developer -> qa-reviewer")

    return 0


if __name__ == "__main__":
    sys.exit(main())
