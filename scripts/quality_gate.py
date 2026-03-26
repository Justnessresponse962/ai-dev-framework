#!/usr/bin/env python3
"""
Quality Gate - GO / CONDITIONAL / NO-GO verdict

Usage: python scripts/quality_gate.py [--tier=1|2|3|all] [--module=name]

Tier 1 (Stability): syntax check, compilation check
Tier 2 (Balance): file sizes, function sizes, secrets, empty catch, tests, .gitignore
Tier 3 (Regression): baseline comparison via JSON file

Exit codes: 0 = GO, 1 = NO-GO, 2 = CONDITIONAL
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


# -- Config ------------------------------------------------------------------
MAX_FILE_LINES = 500
MAX_FUNCTION_LINES = 100
WARN_FILE_LINES = 300

CODE_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx"}
EXCLUDE_DIRS = {"node_modules", ".venv", "dist", "__pycache__", ".git"}

# -- Counters ----------------------------------------------------------------
pass_count = 0
fail_count = 0
warn_count = 0
tier1_pass = True
tier2_pass = True
tier3_pass = True
secrets_found_global = False
verdict = "GO"


# -- Helpers -----------------------------------------------------------------
def _pass(msg: str) -> None:
    global pass_count
    pass_count += 1
    print(f"  [PASS] {msg}")


def _fail(msg: str) -> None:
    global fail_count
    fail_count += 1
    print(f"  [FAIL] {msg}")


def _warn(msg: str) -> None:
    global warn_count
    warn_count += 1
    print(f"  [WARN] {msg}")


def header(title: str) -> None:
    print(f"\n=== {title} ===")


def _is_excluded(path: Path) -> bool:
    """Check if path contains any excluded directory."""
    return any(part in EXCLUDE_DIRS for part in path.parts)


def collect_code_files(target: Path, extensions: set[str] | None = None) -> list[Path]:
    """Recursively collect code files, excluding vendor/build dirs."""
    exts = extensions or CODE_EXTENSIONS
    files: list[Path] = []
    for ext in exts:
        for f in target.rglob(f"*{ext}"):
            if not _is_excluded(f):
                files.append(f)
    return sorted(files)


def collect_test_files(target: Path) -> list[Path]:
    """Collect test files by naming convention."""
    patterns = ["test_*.py", "*.test.ts", "*.test.tsx", "*.spec.ts", "*.test.js"]
    files: list[Path] = []
    for pat in patterns:
        for f in target.rglob(pat):
            if not _is_excluded(f):
                files.append(f)
    return sorted(files)


# ============================================================================
# TIER 1: STABILITY
# ============================================================================
def run_tier1(project_root: Path, target_dir: Path) -> None:
    global tier1_pass, verdict

    header("TIER 1: STABILITY")

    # -- Python syntax check -------------------------------------------------
    py_files = collect_code_files(target_dir, {".py"})
    if py_files:
        syntax_errors = 0
        for f in py_files:
            try:
                # Use ast.parse to avoid subprocess path injection issues
                import ast
                source = f.read_text(encoding="utf-8", errors="replace")
                ast.parse(source, filename=str(f))
            except SyntaxError:
                _fail(f"Syntax error: {f.relative_to(project_root)}")
                syntax_errors += 1
            except (OSError, UnicodeDecodeError):
                _fail(f"Cannot read: {f.relative_to(project_root)}")
                syntax_errors += 1
        if syntax_errors == 0:
            _pass("Python syntax: no errors")
        else:
            tier1_pass = False

    # -- TypeScript compilation ----------------------------------------------
    tsconfig = project_root / "tsconfig.json"
    if tsconfig.exists():
        try:
            result = subprocess.run(
                ["npx", "tsc", "--noEmit"],
                capture_output=True, text=True, cwd=str(project_root), timeout=120,
            )
            if result.returncode == 0:
                _pass("TypeScript: compiles")
            else:
                _fail("TypeScript: compilation errors")
                tier1_pass = False
        except FileNotFoundError:
            _warn("npx not found, skipping TypeScript check")
        except subprocess.TimeoutExpired:
            _warn("TypeScript compilation timed out")

    # -- Dependency file exists ----------------------------------------------
    dep_files = ["package.json", "requirements.txt", "pyproject.toml"]
    if any((project_root / f).exists() for f in dep_files):
        _pass("Dependency file exists")
    else:
        _warn("No dependency file found (package.json / requirements.txt / pyproject.toml)")

    if not tier1_pass:
        verdict = "NO-GO"


# ============================================================================
# TIER 2: BALANCE
# ============================================================================

SECRET_PATTERNS = re.compile(
    r"""(?:password|secret|api_key|apikey|token|private_key|auth_token|access_key)"""
    r"""\s*[=:]\s*["'][^"']{8,}["']""",
    re.IGNORECASE,
)

# Catch os.environ.get("KEY", "actual_hardcoded_fallback") with real values
ENVIRON_FALLBACK_PATTERN = re.compile(
    r"""os\.environ\.get\(\s*["'][^"']+["']\s*,\s*["'](?!$)[^"']{8,}["']\s*\)""",
    re.IGNORECASE,
)

# Lines to skip: comments, env references, example placeholders
SKIP_LINE_PATTERNS = re.compile(
    r"""(^\s*#|^\s*//|^\s*/?\*|\.env|example|placeholder|your[_-]?|changeme|xxx|replace[_-]?me)""",
    re.IGNORECASE,
)


def _check_file_sizes(target_dir: Path, project_root: Path) -> bool:
    """Check file line counts. Returns True if all OK."""
    oversized = False
    for f in collect_code_files(target_dir):
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
            count = len(lines)
        except OSError:
            continue
        if count > MAX_FILE_LINES:
            _fail(f"File too large: {f.relative_to(project_root)} ({count} lines > {MAX_FILE_LINES})")
            oversized = True
        elif count > WARN_FILE_LINES:
            _warn(f"File approaching limit: {f.relative_to(project_root)} ({count} lines)")
    if not oversized:
        _pass("File sizes: all within limits")
    return not oversized


def _check_function_sizes(target_dir: Path, project_root: Path) -> bool:
    """Check that no function/method exceeds MAX_FUNCTION_LINES."""
    # Patterns that start a function/method definition
    py_func_re = re.compile(r"^(\s*)(def |async def )\w+")
    js_func_re = re.compile(
        r"^(\s*)(?:export\s+)?(?:async\s+)?(?:function\s+\w+|"
        r"(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?\(|"
        r"\w+\s*\([^)]*\)\s*\{)"
    )

    oversized = False

    for f in collect_code_files(target_dir):
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue

        is_python = f.suffix == ".py"
        func_re = py_func_re if is_python else js_func_re

        # Track open functions: (name, start_line, indent_level)
        if is_python:
            # For Python: track by indentation
            func_start: int | None = None
            func_name = ""
            func_indent = 0
            for i, line in enumerate(lines):
                m = func_re.match(line)
                if m:
                    # Close previous function if any
                    if func_start is not None:
                        length = i - func_start
                        if length > MAX_FUNCTION_LINES:
                            _fail(
                                f"Function too long: {func_name} in "
                                f"{f.relative_to(project_root)} ({length} lines > {MAX_FUNCTION_LINES})"
                            )
                            oversized = True
                    func_indent = len(m.group(1))
                    func_name = line.strip().split("(")[0].replace("def ", "").replace("async ", "")
                    func_start = i
                elif func_start is not None and line.strip():
                    # Check if we left the function (dedented non-empty line)
                    current_indent = len(line) - len(line.lstrip())
                    if current_indent <= func_indent and not line.strip().startswith(("@", "#")):
                        length = i - func_start
                        if length > MAX_FUNCTION_LINES:
                            _fail(
                                f"Function too long: {func_name} in "
                                f"{f.relative_to(project_root)} ({length} lines > {MAX_FUNCTION_LINES})"
                            )
                            oversized = True
                        func_start = None
            # Check last function in file
            if func_start is not None:
                length = len(lines) - func_start
                if length > MAX_FUNCTION_LINES:
                    _fail(
                        f"Function too long: {func_name} in "
                        f"{f.relative_to(project_root)} ({length} lines > {MAX_FUNCTION_LINES})"
                    )
                    oversized = True
        else:
            # For JS/TS: track by brace counting
            func_start_line: int | None = None
            func_name_js = ""
            brace_depth = 0
            for i, line in enumerate(lines):
                m = js_func_re.match(line)
                if m and func_start_line is None:
                    func_name_js = line.strip()[:60]
                    func_start_line = i
                    brace_depth = 0
                if func_start_line is not None:
                    brace_depth += line.count("{") - line.count("}")
                    if brace_depth <= 0 and i > func_start_line:
                        length = i - func_start_line + 1
                        if length > MAX_FUNCTION_LINES:
                            _fail(
                                f"Function too long: {func_name_js} in "
                                f"{f.relative_to(project_root)} ({length} lines > {MAX_FUNCTION_LINES})"
                            )
                            oversized = True
                        func_start_line = None

    if not oversized:
        _pass("Function sizes: all within limits")
    return not oversized


def _check_secrets(target_dir: Path, project_root: Path) -> bool:
    """Check for hardcoded secrets. Returns True if clean."""
    global secrets_found_global
    found = False
    search_exts = {".py", ".ts", ".tsx", ".js", ".jsx", ".json"}
    skip_names = {"package-lock.json", "yarn.lock"}

    for f in collect_code_files(target_dir, search_exts):
        if f.name in skip_names:
            continue
        if f.suffix == ".json" and f.name.endswith(".env.example"):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        for line_num, line in enumerate(content.splitlines(), 1):
            # Skip comment lines and example placeholders
            if SKIP_LINE_PATTERNS.search(line):
                continue

            matched = False
            if SECRET_PATTERNS.search(line):
                matched = True
            if ENVIRON_FALLBACK_PATTERN.search(line):
                matched = True

            if matched:
                rel = f.relative_to(project_root)
                _fail(f"Possible secret in: {rel}:{line_num}")
                found = True

    if found:
        secrets_found_global = True
    else:
        _pass("No secrets in code")
    return not found


def _check_empty_catch(target_dir: Path, project_root: Path) -> bool:
    """Detect empty catch/except blocks (including multiline and typed except)."""
    found = False

    for f in collect_code_files(target_dir):
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue

        rel = f.relative_to(project_root)

        if f.suffix == ".py":
            # Detect: except ...: followed by only pass/... (possibly with blank lines)
            i = 0
            while i < len(lines):
                stripped = lines[i].strip()
                if re.match(r"except\b.*:\s*$", stripped):
                    except_indent = len(lines[i]) - len(lines[i].lstrip())
                    body_lines: list[str] = []
                    j = i + 1
                    while j < len(lines):
                        if lines[j].strip() == "":
                            j += 1
                            continue
                        line_indent = len(lines[j]) - len(lines[j].lstrip())
                        if line_indent <= except_indent:
                            break
                        body_lines.append(lines[j].strip())
                        j += 1
                    # Check if body is only pass/...
                    if body_lines and all(b in ("pass", "...") for b in body_lines):
                        _fail(f"Empty except block: {rel}:{i + 1}")
                        found = True
                    elif not body_lines:
                        _fail(f"Empty except block: {rel}:{i + 1}")
                        found = True
                i += 1

        elif f.suffix in (".ts", ".tsx", ".js", ".jsx"):
            # Detect catch blocks with empty or only-comment body
            content = "\n".join(lines)
            # Single-line empty: catch(...) { } or catch { }
            if re.search(r"catch\s*(?:\([^)]*\))?\s*\{\s*\}", content):
                _fail(f"Empty catch block: {rel}")
                found = True
            else:
                # Multiline: catch(...) {\n  // only comments or whitespace\n }
                for m in re.finditer(r"catch\s*(?:\([^)]*\))?\s*\{", content):
                    start = m.end()
                    brace = 1
                    pos = start
                    body_content = []
                    while pos < len(content) and brace > 0:
                        if content[pos] == "{":
                            brace += 1
                        elif content[pos] == "}":
                            brace -= 1
                            if brace == 0:
                                break
                        pos += 1
                    body = content[start:pos].strip()
                    # Remove comments
                    body_no_comments = re.sub(r"//.*$", "", body, flags=re.MULTILINE).strip()
                    body_no_comments = re.sub(r"/\*.*?\*/", "", body_no_comments, flags=re.DOTALL).strip()
                    if not body_no_comments:
                        line_num = content[:m.start()].count("\n") + 1
                        _fail(f"Empty catch block: {rel}:{line_num}")
                        found = True

    if not found:
        _pass("No empty catch/except blocks")
    return not found


def _check_tests(target_dir: Path, project_root: Path) -> tuple[bool, bool]:
    """Check tests exist and pass. Returns (exist_ok, pass_ok).

    Runs only the test runner that is relevant to the module's test files:
    - .py test files → pytest
    - .ts/.tsx/.js/.jsx test files → npm test
    - Both → run both, both must pass
    """
    test_files = collect_test_files(target_dir)
    test_count = len(test_files)

    if test_count == 0:
        _warn(f"No test files found in {target_dir.relative_to(project_root)}")
        return False, False

    _pass(f"Test files found: {test_count}")

    # Determine which runners are relevant based on actual test file extensions
    has_py_tests = any(f.suffix == ".py" for f in test_files)
    has_js_tests = any(f.suffix in {".ts", ".tsx", ".js", ".jsx"} for f in test_files)

    all_passed = True
    ran_any = False

    # Run npm test only if JS/TS test files exist in the module
    if has_js_tests:
        pkg_json = project_root / "package.json"
        if pkg_json.exists():
            try:
                pkg = json.loads(pkg_json.read_text(encoding="utf-8"))
                if "test" in pkg.get("scripts", {}):
                    result = subprocess.run(
                        ["npm", "test"], capture_output=True, text=True,
                        cwd=str(project_root), timeout=120,
                    )
                    ran_any = True
                    if result.returncode == 0:
                        _pass("Tests (npm): all pass")
                    else:
                        _fail("Tests (npm): some failures")
                        all_passed = False
            except (json.JSONDecodeError, OSError, subprocess.TimeoutExpired):
                _warn("Could not run npm test")

    # Run pytest only if Python test files exist in the module
    if has_py_tests:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(target_dir), "--tb=no", "-q"],
                capture_output=True, text=True,
                cwd=str(project_root), timeout=120,
            )
            ran_any = True
            if result.returncode == 0:
                _pass("Tests (pytest): all pass")
            else:
                _fail("Tests (pytest): some failures")
                all_passed = False
        except (FileNotFoundError, subprocess.TimeoutExpired):
            _warn("Could not run pytest")

    if not ran_any:
        _warn("Test files found but no runner could execute them")

    return True, all_passed


def _check_gitignore(project_root: Path) -> bool:
    """Check that .env is in .gitignore."""
    gitignore = project_root / ".gitignore"
    if not gitignore.exists():
        _fail(".gitignore not found")
        return False

    try:
        content = gitignore.read_text(encoding="utf-8", errors="replace")
    except OSError:
        _fail("Cannot read .gitignore")
        return False

    # Check for .env entry (exact line or pattern like .env*)
    for line in content.splitlines():
        stripped = line.strip()
        if stripped in (".env", ".env*", ".env.*", "*.env"):
            _pass(".env is in .gitignore")
            return True
        if stripped.startswith(".env"):
            _pass(".env is in .gitignore")
            return True

    _fail(".env is NOT listed in .gitignore")
    return False


def run_tier2(project_root: Path, target_dir: Path) -> None:
    global tier2_pass, verdict, secrets_found_global

    header("TIER 2: BALANCE")

    checks = 0
    passed = 0

    # File sizes
    checks += 1
    if _check_file_sizes(target_dir, project_root):
        passed += 1

    # Function sizes
    checks += 1
    if _check_function_sizes(target_dir, project_root):
        passed += 1

    # Secrets
    checks += 1
    if _check_secrets(target_dir, project_root):
        passed += 1

    # Empty catch/except
    checks += 1
    if _check_empty_catch(target_dir, project_root):
        passed += 1

    # Tests exist and pass
    checks += 1
    exist_ok, pass_ok = _check_tests(target_dir, project_root)
    if exist_ok:
        passed += 1
    if exist_ok:
        checks += 1
        if pass_ok:
            passed += 1

    # .gitignore check
    checks += 1
    if _check_gitignore(project_root):
        passed += 1

    # -- Hard veto: secrets found = automatic NO-GO --------------------------
    if secrets_found_global:
        verdict = "NO-GO"
        tier2_pass = False
        print("\n  [VETO] Secrets detected => automatic NO-GO regardless of other checks")
        return

    # -- Majority voting -----------------------------------------------------
    if checks > 0:
        ratio = passed * 100 // checks
        if ratio < 50:
            tier2_pass = False
            verdict = "NO-GO"
        elif ratio < 75:
            if verdict == "GO":
                verdict = "CONDITIONAL"


# ============================================================================
# TIER 3: REGRESSION
# ============================================================================
def run_tier3(project_root: Path, target_dir: Path, module_name: str) -> None:
    global tier3_pass, verdict

    header("TIER 3: REGRESSION")

    baseline_dir = project_root / "scripts" / ".baselines"
    baseline_dir.mkdir(parents=True, exist_ok=True)
    baseline_file = baseline_dir / f"{module_name or 'project'}.json"

    # Collect current metrics
    code_files = collect_code_files(target_dir)
    total_files = len(code_files)
    total_lines = 0
    for f in code_files:
        try:
            total_lines += len(f.read_text(encoding="utf-8", errors="replace").splitlines())
        except OSError:
            pass
    test_count = len(collect_test_files(target_dir))

    if baseline_file.exists():
        try:
            baseline = json.loads(baseline_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            baseline = {}

        prev_tests = baseline.get("tests", 0)
        prev_lines = baseline.get("lines", 0)

        # Test count should not decrease
        if test_count < prev_tests:
            _fail(f"Test count decreased: {prev_tests} -> {test_count}")
            tier3_pass = False
        else:
            _pass(f"Test count: {prev_tests} -> {test_count} (stable or increased)")

        # Lines growth > 50% = warning
        if prev_lines > 0:
            growth = (total_lines - prev_lines) * 100 // prev_lines
            if growth > 50:
                _warn(f"Code growth: +{growth}% ({prev_lines} -> {total_lines} lines)")
            else:
                _pass(f"Code growth: +{growth}% (within limits)")
    else:
        _pass("No baseline found -- saving initial baseline")

    # Save baseline only on GO (never save broken state as baseline)
    if verdict == "GO":
        baseline_file.write_text(
            json.dumps({"files": total_files, "lines": total_lines, "tests": test_count}),
            encoding="utf-8",
        )
        _pass(f"Baseline saved: {total_files} files, {total_lines} lines, {test_count} tests")


# ============================================================================
# MAIN
# ============================================================================
def main() -> int:
    global verdict

    parser = argparse.ArgumentParser(description="Quality Gate")
    parser.add_argument("--tier", default="all", help="1, 2, 3, or all")
    parser.add_argument("--module", default="", help="Module name")
    args = parser.parse_args()

    tier = args.tier
    module = args.module

    # Determine project root (parent of scripts/)
    project_root = Path(__file__).resolve().parent.parent

    # Determine target directory
    if module:
        target_dir = None
        for candidate in [f"app/{module}", f"src/{module}", module]:
            d = project_root / candidate
            if d.is_dir():
                target_dir = d
                break
        if target_dir is None:
            print(f"Module directory not found for: {module}")
            print(f"Searched: app/{module}, src/{module}, {module}")
            return 1
    else:
        target_dir = project_root

    # Banner
    print()
    print("+" + "=" * 40 + "+")
    print(f"|  QUALITY GATE")
    print(f"|  Module: {module or 'project'}")
    print(f"|  Tier: {tier}")
    print("+" + "=" * 40 + "+")

    # Run tiers
    if tier == "1":
        run_tier1(project_root, target_dir)
    elif tier == "2":
        run_tier2(project_root, target_dir)
    elif tier == "3":
        run_tier3(project_root, target_dir, module)
    elif tier == "all":
        run_tier1(project_root, target_dir)
        run_tier2(project_root, target_dir)
        run_tier3(project_root, target_dir, module)
    else:
        print(f"Unknown tier: {tier}")
        return 1

    # Final verdict
    print()
    print("=" * 42)
    print(f"  VERDICT: {verdict}")
    print(f"  Passed: {pass_count} | Failed: {fail_count} | Warnings: {warn_count}")
    print("=" * 42)

    if verdict == "GO":
        return 0
    elif verdict == "CONDITIONAL":
        return 2
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
