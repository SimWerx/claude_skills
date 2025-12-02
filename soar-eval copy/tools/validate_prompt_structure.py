#!/usr/bin/env python3
"""
Validate required sections exist in LLM judge prompts.

Usage:
    python tools/validate_prompt_structure.py
    python tools/validate_prompt_structure.py --file evaluators/llm-judge/negation_simple_prompt.md

Checks:
    1. All required sections present (SYSTEM, BEHAVIOR, DESCRIPTION, etc.)
    2. All RUBRIC subsections present
    3. Output schema instruction present

Exit codes:
    0 = All prompts pass
    1 = One or more prompts have missing sections
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PROMPTS_DIR = PROJECT_ROOT / "evaluators" / "llm-judge"

# Required sections in order of appearance
REQUIRED_SECTIONS = [
    ("SYSTEM:", "Standard system prompt"),
    ("BEHAVIOR:", "Behavior identifier"),
    ("DESCRIPTION:", "Behavior description"),
    ("EVALUATION SCOPE:", "Scope header"),
    ("Include:", "Include list"),
    ("Ignore:", "Ignore list"),
    ("RUBRIC", "Rubric header"),
    ("Automatic fail if any of the following are true:", "Automatic fail section"),
    ("Pass conditions (all must be satisfied):", "Pass conditions section"),
    ("Acceptable variations (still treated as pass):", "Acceptable variations section"),
    ("Uncertainty policy:", "Uncertainty policy section"),
]

OUTPUT_SCHEMA_PATTERN = '{"pass":'


def check_prompt(path: Path) -> list[str]:
    """Return list of missing sections with descriptions."""
    content = path.read_text()
    missing = []
    
    for section, description in REQUIRED_SECTIONS:
        if section not in content:
            missing.append(f"{description} ('{section}')")
    
    # Check output schema
    if OUTPUT_SCHEMA_PATTERN not in content:
        missing.append("Output schema instruction ('{\"pass\":...')")
    
    return missing


def main():
    parser = argparse.ArgumentParser(description="Validate LLM judge prompt structure")
    parser.add_argument("--file", type=str, help="Check single file (relative to project root)")
    args = parser.parse_args()
    
    if args.file:
        # Single file mode
        path = PROJECT_ROOT / args.file
        if not path.exists():
            print(f"ERROR: File not found: {path}")
            sys.exit(1)
        
        missing = check_prompt(path)
        if missing:
            print(f"FAIL: {path.name}")
            for m in missing:
                print(f"  - Missing: {m}")
            sys.exit(1)
        else:
            print(f"PASS: {path.name}")
            sys.exit(0)
    
    # All prompts mode
    prompt_files = sorted(PROMPTS_DIR.glob("*_prompt.md"))
    issues = []
    
    for prompt_file in prompt_files:
        missing = check_prompt(prompt_file)
        if missing:
            issues.append((prompt_file.name, missing))
    
    # Output
    print(f"Checked {len(prompt_files)} prompt files\n")
    
    if issues:
        print(f"FAIL: {len(issues)} prompts have missing sections:\n")
        for filename, missing in issues:
            print(f"  {filename}:")
            for m in missing:
                print(f"    - {m}")
        sys.exit(1)
    else:
        print("PASS: All prompts have required sections.")
        sys.exit(0)


if __name__ == "__main__":
    main()

