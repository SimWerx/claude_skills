#!/usr/bin/env python3
"""
Flag prompts that may have AND/OR logic issues in Automatic fail section.

Usage:
    python tools/flag_compound_logic.py
    python tools/flag_compound_logic.py --verbose

Purpose:
    Surfaces prompts for manual review where "Automatic fail" bullets may be
    incorrectly split compound AND conditions. This is a heuristic flagger,
    not a definitive validator.

Heuristics:
    - Multiple bullets without explicit "AND" = potential split compound
    - Single bullet with "AND" = likely correct compound condition
    - Prompts with 1 bullet or all bullets containing AND = low risk

Exit codes:
    0 = No candidates flagged (or only low-risk patterns)
    1 = Candidates flagged for review (informational, not blocking)
"""

import argparse
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PROMPTS_DIR = PROJECT_ROOT / "evaluators" / "llm-judge"


def extract_auto_fail_bullets(content: str) -> list[str]:
    """Extract bullet items from Automatic fail section."""
    match = re.search(
        r'Automatic fail if any of the following are true:\n((?:- .+\n?)+)',
        content,
        re.MULTILINE
    )
    if not match:
        return []
    
    bullets_text = match.group(1)
    # Split on newline-dash pattern, keeping content
    raw_bullets = re.split(r'\n- ', bullets_text)
    # Clean up: remove leading dash from first, strip all
    bullets = []
    for i, b in enumerate(raw_bullets):
        cleaned = b.strip()
        if i == 0:
            cleaned = cleaned.lstrip('- ')
        if cleaned and not cleaned.startswith('Example:'):  # Skip example lines
            bullets.append(cleaned)
    
    return bullets


def analyze_prompt(path: Path) -> dict:
    """Analyze a prompt for AND/OR logic patterns."""
    content = path.read_text()
    bullets = extract_auto_fail_bullets(content)
    
    result = {
        "filename": path.name,
        "bullet_count": len(bullets),
        "bullets_with_and": sum(1 for b in bullets if " AND " in b),
        "risk_level": "low",
        "flags": [],
        "bullets": bullets,
    }
    
    if len(bullets) == 0:
        result["flags"].append("No Automatic fail bullets found")
        result["risk_level"] = "review"
        return result
    
    if len(bullets) == 1:
        # Single bullet - likely fine
        return result
    
    # Multiple bullets
    if result["bullets_with_and"] == 0:
        # Multiple bullets, none with AND - potential issue
        result["flags"].append(
            f"{len(bullets)} bullets without explicit AND - verify these are independent failure modes"
        )
        result["risk_level"] = "review"
    elif result["bullets_with_and"] < len(bullets):
        # Mixed - some have AND, some don't
        result["flags"].append(
            f"{result['bullets_with_and']}/{len(bullets)} bullets have AND - verify consistency"
        )
        result["risk_level"] = "review"
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Flag AND/OR logic candidates for review")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show bullet content")
    args = parser.parse_args()
    
    prompt_files = sorted(PROMPTS_DIR.glob("*_prompt.md"))
    
    results = []
    for prompt_file in prompt_files:
        result = analyze_prompt(prompt_file)
        results.append(result)
    
    # Separate by risk level
    review_needed = [r for r in results if r["risk_level"] == "review"]
    low_risk = [r for r in results if r["risk_level"] == "low"]
    
    print(f"Analyzed {len(results)} prompt files\n")
    print(f"Low risk (single bullet or all have AND): {len(low_risk)}")
    print(f"Review candidates: {len(review_needed)}\n")
    
    if review_needed:
        print("=" * 60)
        print("CANDIDATES FOR MANUAL AND/OR LOGIC REVIEW")
        print("=" * 60)
        print()
        
        for r in review_needed:
            print(f"{r['filename']} ({r['bullet_count']} bullets, {r['bullets_with_and']} with AND)")
            for flag in r["flags"]:
                print(f"  > {flag}")
            
            if args.verbose and r["bullets"]:
                print("  Bullets:")
                for b in r["bullets"]:
                    truncated = b[:100] + "..." if len(b) > 100 else b
                    has_and = " [AND]" if " AND " in b else ""
                    print(f"    - {truncated}{has_and}")
            print()
        
        print("-" * 60)
        print("NOTE: This is a heuristic flag, not a definitive error.")
        print("Review each candidate to verify OR logic is intentional.")
        print("-" * 60)
    
    # Exit 0 always - this is informational, not blocking
    sys.exit(0)


if __name__ == "__main__":
    main()

