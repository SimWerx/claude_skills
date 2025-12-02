#!/usr/bin/env python3
"""validate_benchmark_criteria.py - Verify inclusion/exclusion criteria follow spec format.

Checks that:
- inclusion_criteria contains "Apply when" AND "Flag if"
- exclusion_criteria contains "Do not apply" OR "Do not use"

Per benchmarks/FIELD_SPECS.md specification.
"""

import re
import sys
from pathlib import Path


def check_benchmark(path: Path) -> list[str]:
    """Return list of format issues for a benchmark file."""
    content = path.read_text()
    issues = []
    
    # Check inclusion_criteria
    # Pattern allows internal blank lines within YAML folded scalars
    inc_match = re.search(r'inclusion_criteria:\s*>\s*\n((?:[ \t]+.*\n|\n)+)', content)
    if not inc_match:
        issues.append("Missing inclusion_criteria field")
    else:
        inc_text = inc_match.group(1)
        if "Apply when" not in inc_text:
            issues.append("inclusion_criteria: Missing 'Apply when' clause")
        if "Flag if" not in inc_text:
            issues.append("inclusion_criteria: Missing 'Flag if' clause")
    
    # Check exclusion_criteria
    # Pattern allows internal blank lines within YAML folded scalars
    exc_match = re.search(r'exclusion_criteria:\s*>\s*\n((?:[ \t]+.*\n|\n)+)', content)
    if not exc_match:
        issues.append("Missing exclusion_criteria field")
    else:
        exc_text = exc_match.group(1)
        if "Do not apply" not in exc_text and "Do not use" not in exc_text:
            issues.append("exclusion_criteria: Missing 'Do not apply' or 'Do not use' clause")
    
    return issues


def main():
    # Determine benchmark directory relative to script or workspace
    script_dir = Path(__file__).parent.parent
    benchmark_dir = script_dir / "benchmarks" / "a-component"
    
    if not benchmark_dir.exists():
        # Try from workspace root
        benchmark_dir = Path("zy_experimental/soar-pydantic-eval/benchmarks/a-component")
    
    if not benchmark_dir.exists():
        print(f"Error: Cannot find benchmark directory")
        sys.exit(1)
    
    problems = []
    checked = 0
    
    for yaml_file in sorted(benchmark_dir.glob("*.yaml")):
        if yaml_file.name in ["NONE.yaml"]:  # Skip special files
            continue
        checked += 1
        issues = check_benchmark(yaml_file)
        if issues:
            problems.append((yaml_file.name, issues))
    
    if problems:
        print("Benchmark criteria format issues:\n")
        for filename, issues in problems:
            print(f"{filename}:")
            for issue in issues:
                print(f"  - {issue}")
        print(f"\n{len(problems)} of {checked} benchmarks have issues.")
        sys.exit(1)
    else:
        print(f"PASS: All {checked} benchmarks have valid criteria format.")


if __name__ == "__main__":
    main()

