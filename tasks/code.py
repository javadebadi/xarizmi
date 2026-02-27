"""Reusable code quality tasks for Python projects."""

import webbrowser
from pathlib import Path

from invoke.collection import Collection
from invoke.context import Context
from invoke.tasks import task


def _complexity_threshold_to_grade(threshold: int) -> str:
    """Convert numeric complexity threshold to radon grade for violations.

    For a given threshold T, returns the minimum grade to show functions
    with complexity > T.

    Radon grades:
    A: 1-5, B: 6-10, C: 11-20, D: 21-30, E: 31-40, F: 41+
    """
    if threshold >= 41 or threshold >= 31:
        return "F"
    elif threshold >= 21:
        return "E"
    elif threshold >= 11:
        return "D"
    elif threshold >= 6:
        return "C"
    else:
        return "B"


def _run_format(c: Context, path: str = ".") -> None:
    c.run(f"ruff format {path}")


def _run_black(c: Context, path: str = ".") -> None:
    c.run(f"black {path}")


@task(help={"path": "Path to folder to autoformat its code."})
def autoformat(c: Context, path: str = ".") -> None:
    """Lint and autofix code with ruff and black."""
    _run_black(c, path=path)
    _run_format(c, path=path)
    cmd = f"ruff check {path} --fix"
    c.run(cmd, pty=True)


@task(help={"path": "Path to folder to run ruff check on."})
def check(c: Context, path: str = ".") -> None:
    """
    Check if code is already formatted / lint-fixed.
    Fails (non-zero exit) if any issues are present.
    """
    # Ruff check only (no --fix), it will return non-zero if issues exist
    format_result = c.run(f"ruff format --diff {path}", pty=True)
    lint_result = c.run(f"ruff check {path}", pty=True)
    if (format_result and format_result.exited != 0) or (
        lint_result and lint_result.exited != 0
    ):
        print(
            "❌ Code is not properly formatted or linted. "
            "Run `invoke code.autoformat` to fix.",
        )
        exit(1)
    else:
        print("✅ Code is properly formatted and linted.")


@task(help={"path": "Path to tests or test folder."})
def mypy(c: Context, path: str = ".") -> None:
    """Run mypy type checking."""
    c.run(f"mypy {path}", pty=True)


@task(help={"path": "Path to tests or test folder."})
def ty(c: Context, path: str = ".") -> None:
    """Run ty type checking (informational; no Pydantic plugin yet)."""
    c.run(f"ty check {path}", pty=True, warn=True)


@task(help={"path": "Path to tests or test folder."})
def test(c: Context, path: str = ".", env: str = "TEST") -> None:
    """
    Run pytest on test suite.

    Args:
        path: Path to tests
        env: Environment variable value for ENVIRONMENT
    """
    c.run(
        f"export ENVIRONMENT={env};pytest -vv {path}|| [ $? -eq 5 ]", pty=True
    )


@task(help={})
def coverage(c: Context, path: str = ".", env: str = "TEST") -> None:
    """
    Run pytest coverage on test suite and generate HTML report.

    Args:
        path: Coverage path (default: .)
        env: Environment variable value
    """
    c.run(f"export ENVIRONMENT={env};pytest --cov={path}", pty=True)
    c.run(f"export ENVIRONMENT={env};coverage html")


@task(help={})
def coverage_open(c: Context, path: str = ".", env: str = "TEST") -> None:
    """
    Run pytest coverage, generate HTML report, and open in browser.
    """
    coverage(c, path=path, env=env)

    # Open in default browser (cross-platform)
    report_path = Path("htmlcov/index.html").absolute()
    if report_path.exists():
        webbrowser.open(f"file://{report_path}")
    else:
        print("Coverage report not found at htmlcov/index.html")


@task(help={})
def coverage_xml(
    c: Context,
    path: str = ".",
) -> None:
    """
    Run pytest coverage on test suite and generate XML report.

    Args:
        path: Coverage path (default: .)
    """
    c.run(f"pytest --cov={path} --cov-report=xml", pty=True)


@task(help={})
def coverage_score(c: Context, path: str = ".", env: str = "TEST") -> None:
    """Get single coverage score as percentage."""
    cmd = (
        f"export ENVIRONMENT={env};"
        f"pytest --cov={path} -q 2>&1 | grep 'TOTAL' | awk '{{print $NF}}'"
    )
    result = c.run(cmd, pty=False, hide=True)
    if result and result.stdout:
        score = result.stdout.strip()
        print(f"Coverage: {score}")
    else:
        print("Could not determine coverage score")


@task(help={"path": "Path to tests or test folder."})
def ci(c: Context, path: str = ".", env: str = "TEST") -> None:
    """
    Run Continuous Integration tasks.

    Includes: autoformat, check, ty, mypy, complexity, test.
    """
    autoformat(c, path=path)
    check(c, path=path)
    ty(c, path=path)
    mypy(c, path=path)
    complexity(c)
    test(c, path=path, env=env)


@task(help={})
def security(c: Context, path: str = ".") -> None:
    """
    Run security scans on code and dependencies.

    Checks for:
    - Code security issues with bandit
    - Dependency vulnerabilities with pip-audit

    Args:
        path: Path to scan for security issues (default: .)
    """
    print("🔒 Running security scans...\n")

    print("📝 Scanning code for security issues (bandit)...")
    # -r: recursive, -ll: only show high+medium severity
    # -f: format (screen for terminal output)
    result = c.run(f"bandit -r {path} -ll -f screen", warn=True, pty=True)

    print("\n📦 Checking dependencies for vulnerabilities (pip-audit)...")
    audit_result = c.run("pip-audit", warn=True, pty=True)

    # Determine overall result
    if (result and result.exited != 0) or (
        audit_result and audit_result.exited != 0
    ):
        print("\n❌ Security issues found! Review the output above.")
        exit(1)
    else:
        print("\n✅ No security issues detected!")


@task(help={})
def osv_scan(c: Context) -> None:
    """
    Scan dependencies for known vulnerabilities using OSV-Scanner.

    Checks the uv.lock lockfile against the OSV database for known
    vulnerabilities in project dependencies.
    """
    print("🔍 Running OSV-Scanner for dependency vulnerabilities...\n")

    result = c.run("osv-scanner scan --lockfile=uv.lock", warn=True, pty=True)

    if result is not None and result.exited != 0:
        print(
            "\n❌ OSV-Scanner found vulnerabilities! Review the output above."
        )
        exit(1)
    else:
        print("\n✅ No known vulnerabilities detected by OSV-Scanner!")


@task(
    help={
        "path": "Path to analyze (default: .)",
        "max_complexity": "Maximum cyclomatic complexity (default: 15)",
        "min_maintainability": "Minimum maintainability index (default: 65)",
        "verbose": "Show detailed complexity report (default: False)",
    },
)
def complexity(
    c: Context,
    path: str = ".",
    max_complexity: int = 15,
    min_maintainability: int = 65,
    verbose: bool = False,
) -> None:
    """
    Analyze code complexity metrics.

    Checks for:
    - Cyclomatic complexity (McCabe)
    - Maintainability index
    - Shows functions/files that exceed thresholds

    Args:
        path: Path to analyze (default: .)
        max_complexity: Max cyclomatic complexity threshold (default: 15)
        min_maintainability: Min maintainability index threshold (default: 65)
        verbose: Show detailed complexity report (default: False)
    """
    print("📊 Running complexity analysis...")

    if verbose:
        print(
            f"\n🔄 Checking cyclomatic complexity "
            f"(threshold: {max_complexity})..."
        )
        c.run(
            f"radon cc {path} -s -a --total-average",
            warn=True,
            pty=True,
        )

        print(
            f"\n🔧 Checking maintainability index "
            f"(threshold: {min_maintainability})...",
        )
        c.run(
            f"radon mi {path} -s",
            warn=True,
            pty=True,
        )

    # Check if there are high-complexity issues
    print(
        f"\n📈 Checking for complexity violations (max: {max_complexity})..."
    )
    # Convert threshold to grade (radon uses letter grades, not numbers)
    min_violation_grade = _complexity_threshold_to_grade(max_complexity)
    violations_result = c.run(
        f"radon cc {path} --min {min_violation_grade} -s",
        warn=True,
        pty=False,
        hide=True,
    )

    has_violations = False
    if violations_result and violations_result.stdout:
        violations_output = violations_result.stdout.strip()
        # Check if there's actual content (not just whitespace)
        if violations_output:
            print(f"\n⚠️  Found functions with complexity > {max_complexity}:")
            print(violations_output)
            has_violations = True

    if has_violations:
        print(
            f"\n❌ Code complexity issues found! "
            f"Functions exceed maximum complexity of {max_complexity}.",
        )
        print("Consider refactoring complex functions into smaller ones.")
        exit(1)
    else:
        print(
            f"\n✅ All functions are within complexity threshold "
            f"({max_complexity})!",
        )


@task(
    help={
        "path": "Path to analyze (default: .)",
        "min_confidence": "Minimum confidence for dead code (default: 80)",
        "strict": "Fail if dead code found (default: False)",
    },
)
def deadcode(
    c: Context,
    path: str = ".",
    min_confidence: int = 80,
    strict: bool = False,
) -> None:
    """
    Detect dead code (unused functions, classes, variables, imports).

    Uses vulture to find unused code. By default runs in informational mode.
    Use --strict to fail CI on dead code detection.

    Note: May have false positives for:
    - Alembic migrations (upgrade/downgrade functions)
    - FastAPI routes (decorator-based)
    - Pytest fixtures (name-based detection)

    Args:
        path: Path to analyze (default: .)
        min_confidence: Minimum confidence percentage (default: 80)
        strict: Fail CI if dead code found (default: False)
    """
    print("🔍 Running dead code detection...\n")

    # Exclude common false positive patterns
    exclude_patterns = [
        "*/alembic/versions/*",  # Migration files
        "*/conftest.py",  # Pytest configuration
    ]
    exclude_args = " ".join(f'--exclude "{p}"' for p in exclude_patterns)

    # Run vulture with minimum confidence threshold
    result = c.run(
        f"vulture {path} --min-confidence {min_confidence} {exclude_args}",
        warn=True,
        pty=True,
    )

    has_dead_code = result and result.exited != 0

    if has_dead_code:
        print(
            f"\n⚠️  Potential dead code detected! "
            f"Review unused code above (confidence >= {min_confidence}%).",
        )
        print(
            "Note: May include false positives "
            "(FastAPI routes, fixtures, etc.)"
        )
        if strict:
            print("Running in strict mode - failing CI.")
            exit(1)
        else:
            print("Running in informational mode - not failing CI.")
    else:
        print(
            f"\n✅ No dead code detected (confidence >= {min_confidence}%)!",
        )


@task(
    help={
        "path": "Path to analyze (default: .)",
        "min_coverage": "Minimum docstring coverage percentage (default: 80)",
        "strict": "Fail if coverage below threshold (default: False)",
    },
)
def docstrings(
    c: Context,
    path: str = ".",
    min_coverage: int = 80,
    strict: bool = False,
) -> None:
    """
    Check docstring coverage for modules, classes, and functions.

    Uses interrogate to measure documentation coverage.
    By default runs in informational mode.

    Args:
        path: Path to analyze (default: .)
        min_coverage: Minimum coverage percentage (default: 80)
        strict: Fail CI if coverage below threshold (default: False)
    """
    print("📝 Running docstring coverage analysis...\n")

    # Run interrogate with coverage threshold
    # -v: verbose (show missing docstrings)
    # --fail-under: minimum coverage percentage
    # --ignore-init-method: ignore __init__ methods
    # --ignore-private: ignore private methods (_method)
    # --ignore-magic: ignore magic methods (__method__)
    # --exclude: patterns to exclude
    result = c.run(
        f"interrogate {path} "
        f"--fail-under {min_coverage} "
        "--ignore-init-method "
        "--ignore-private "
        "--ignore-magic "
        "--exclude 'alembic' "
        "--exclude 'tests' "
        "-v",
        warn=True,
        pty=True,
    )

    below_threshold = result is not None and result.exited != 0

    if below_threshold:
        print(
            "\n⚠️  Docstring coverage below threshold!",
        )
        if strict:
            print("Running in strict mode - failing CI.")
            exit(1)
        else:
            print("Running in informational mode - not failing CI.")
            print(
                f"Tip: Add docstrings to improve coverage to {min_coverage}%+"
            )
    else:
        print(f"\n✅ Docstring coverage meets threshold ({min_coverage}%)!")


@task(
    help={
        "path": "Path to analyze (default: .)",
        "min_coverage": "Minimum type coverage percentage (default: 80)",
        "open_report": "Open HTML report in browser (default: False)",
        "strict": "Fail if coverage below threshold (default: False)",
    },
)
def typecov(
    c: Context,
    path: str = ".",
    min_coverage: int = 80,
    open_report: bool = False,
    strict: bool = False,
) -> None:
    """
    Measure type annotation coverage with HTML report.

    Generates an HTML report showing which functions/methods have type
    annotations. Useful for tracking type safety improvements.

    Args:
        path: Path to analyze (default: .)
        min_coverage: Minimum coverage percentage (default: 80)
        open_report: Open HTML report in browser (default: False)
        strict: Fail CI if coverage below threshold (default: False)
    """
    print("📊 Measuring type annotation coverage...\n")

    # Generate HTML report with type coverage
    c.run(
        f"mypy {path} --html-report .mypy-coverage --txt-report"
        " .mypy-coverage",
        warn=True,
        pty=False,
    )

    # Parse coverage from text report
    try:
        with open(".mypy-coverage/index.txt") as f:
            content = f.read()
            # Look for Total imprecision percentage in report
            # Mypy reports "imprecision" - coverage = 100 - imprecision
            import re

            # Look for line like: | Total | 7.35% imprecise | 13293 LOC |
            match = re.search(
                r"\|\s*Total\s*\|\s*([\d.]+)%\s*imprecise", content
            )
            if match:
                imprecision = float(match.group(1))
                actual_coverage = 100 - imprecision
                print(f"\n📈 Type coverage: {actual_coverage:.2f}%")
                print(f"    (Imprecision: {imprecision}%)")

                below_threshold = actual_coverage < min_coverage

                if below_threshold:
                    print(f"⚠️  Type coverage below {min_coverage}% threshold!")
                    if strict:
                        print("Running in strict mode - failing CI.")
                        exit(1)
                    else:
                        print(
                            "Running in informational mode - not failing CI."
                        )
                        print("Tip: Add type hints to improve coverage")
                else:
                    print(
                        f"✅ Type coverage meets threshold ({min_coverage}%)!"
                    )
            else:
                print("⚠️  Could not parse coverage from report")
    except FileNotFoundError:
        print("⚠️  Coverage report not generated")

    # Open report in browser if requested
    if open_report:
        report_path = Path(".mypy-coverage/index.html").absolute()
        if report_path.exists():
            webbrowser.open(f"file://{report_path}")
            print(f"\n📂 Opened coverage report: {report_path}")
        else:
            print("\n⚠️  HTML report not found at .mypy-coverage/index.html")


@task(
    help={
        "output_format": "Output format: table, json, csv, markdown"
        " (default: table)",
        "fail_on": "Fail if these licenses found"
        " (comma-separated, e.g., 'GPL,AGPL')",
        "strict": "Fail if any license issues found (default: False)",
    },
)
def licenses(
    c: Context,
    output_format: str = "table",
    fail_on: str = "",
    strict: bool = False,
) -> None:
    """
    Check dependency licenses for compliance.

    Lists all dependencies and their licenses. Optionally fails if specific
    problematic licenses are detected (e.g., GPL variants that require
    open-sourcing derivative works).

    Args:
        output_format: Output format (table, json, csv, markdown)
        fail_on: Comma-separated list of licenses to fail on (e.g., 'GPL,AGPL')
        strict: Fail if any unknown or problematic licenses found
    """
    print("📜 Checking dependency licenses...\n")

    # Run pip-licenses with specified format
    format_flag = (
        f"--format={output_format}" if output_format != "table" else ""
    )
    result = c.run(
        f"pip-licenses {format_flag} --with-urls --summary",
        warn=True,
        pty=True,
    )

    # Check for problematic licenses if fail_on specified
    if fail_on:
        problematic = [lic.strip() for lic in fail_on.split(",")]
        print(
            f"\n🔍 Checking for problematic licenses: {', '.join(problematic)}"
        )

        # Get license list in plain format for parsing
        license_check = c.run(
            "pip-licenses --format=json",
            warn=True,
            pty=False,
            hide=True,
        )

        if license_check and license_check.stdout:
            import json

            licenses_data = json.loads(license_check.stdout)
            found_problematic = []

            for pkg in licenses_data:
                pkg_license = pkg.get("License", "Unknown")
                for prob_lic in problematic:
                    if prob_lic.upper() in pkg_license.upper():
                        found_problematic.append(
                            f"{pkg['Name']} ({pkg_license})",
                        )

            if found_problematic:
                print("\n❌ Found problematic licenses:")
                for item in found_problematic:
                    print(f"  - {item}")
                if strict:
                    print("\nRunning in strict mode - failing CI.")
                    exit(1)
                else:
                    print("\nRunning in informational mode - not failing CI.")
            else:
                print("\n✅ No problematic licenses found!")

    if result and result.exited == 0:
        print("\n✅ License check complete!")
    else:
        print("\n⚠️  Some packages have unknown licenses")
        if strict:
            print("Running in strict mode - failing CI.")
            exit(1)


@task(
    help={
        "path": "Path to analyze (default: .)",
        "min_lines": "Minimum duplicate lines to report (default: 5)",
        "strict": "Fail if duplicates found (default: False)",
    },
)
def duplication(
    c: Context,
    path: str = ".",
    min_lines: int = 5,
    strict: bool = False,
) -> None:
    """
    Detect duplicate/copy-pasted code using pylint.

    Finds code blocks that have been copied and pasted, which can lead to
    maintenance issues when bugs need to be fixed in multiple places.

    Args:
        path: Path to analyze (default: .)
        min_lines: Minimum number of duplicate lines to report (default: 5)
        strict: Fail CI if duplicates found (default: False)
    """
    print("🔍 Detecting code duplication...\n")

    # Run pylint with only duplicate-code checker enabled
    # --disable=all --enable=duplicate-code: only check for duplication
    result = c.run(
        f"pylint --disable=all --enable=duplicate-code "
        f"--min-similarity-lines={min_lines} "
        f"--ignore-patterns=test_.*,conftest.py "
        f"{path}",
        warn=True,
        pty=True,
    )

    has_duplicates = result is not None and result.exited != 0

    if has_duplicates:
        print(
            f"\n⚠️  Code duplication detected! "
            f"Found duplicate code blocks (>= {min_lines} lines).",
        )
        print(
            "Consider refactoring duplicated code into reusable "
            "functions/classes."
        )
        if strict:
            print("Running in strict mode - failing CI.")
            exit(1)
        else:
            print("Running in informational mode - not failing CI.")
    else:
        print(
            f"\n✅ No code duplication detected"
            f" (threshold: {min_lines} lines)!"
        )


@task(help={})
def clean(c: Context) -> None:
    """Remove cached folders."""
    c.run("rm -rf .mypy_cache", pty=True)
    c.run("rm -rf .pytest_cache", pty=True)
    c.run("rm -rf .ruff_cache", pty=True)
    c.run('find . -type d -name "__pycache__" -exec rm -rf {} +', pty=True)
    c.run("rm -rf htmlcov")
    c.run("rm -rf .mypy-coverage")
    c.run("rm -rf *.egg-info")
    c.run("rm -rf site")


@task(help={})
def docs(c: Context) -> None:
    """Build documentation with MkDocs."""
    print("📚 Building documentation...\n")
    c.run("mkdocs build", pty=True)
    print("\n✅ Documentation built successfully in site/")


@task(help={})
def docs_serve(c: Context) -> None:
    """Serve documentation locally with live reload."""
    print("📚 Starting documentation server...\n")
    print("Documentation will be available at http://127.0.0.1:8000")
    print("Press Ctrl+C to stop the server\n")
    c.run("mkdocs serve", pty=True)


# Create collection for export
ns_code = Collection("code")
ns_code.add_task(autoformat)
ns_code.add_task(check)
ns_code.add_task(mypy)
ns_code.add_task(ty)
ns_code.add_task(test)
ns_code.add_task(ci)
ns_code.add_task(security)
ns_code.add_task(osv_scan)
ns_code.add_task(complexity)
ns_code.add_task(deadcode)
ns_code.add_task(docstrings)
ns_code.add_task(typecov)
ns_code.add_task(licenses)
ns_code.add_task(duplication)
ns_code.add_task(clean)
ns_code.add_task(coverage)
ns_code.add_task(coverage_open)
ns_code.add_task(coverage_xml)
ns_code.add_task(coverage_score)
ns_code.add_task(docs)
ns_code.add_task(docs_serve)

__all__ = ["ns_code"]
