#!/usr/bin/env python3
"""
Validate consistency between rubrics, benchmarks, and LLM prompts.

Usage:
    python tools/validate_consistency.py
    python tools/validate_consistency.py --report reports/consistency.md

Checks:
    1. Rubric benchmarks[] → benchmark files exist
    2. Benchmark parent_rubric → rubric file exists
    3. Benchmark llm_prompt_file → prompt file exists
    4. Orphan prompts (not referenced by any benchmark)
    5. Required fields present
    6. Enum values valid
    7. Shared prompts with different thresholds/criticality (single behavior per judge)
"""

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)


# Paths relative to project root
PROJECT_ROOT = Path(__file__).parent.parent
RUBRICS_DIR = PROJECT_ROOT / "rubrics"
BENCHMARKS_DIR = PROJECT_ROOT / "benchmarks" / "a-component"
PROMPTS_DIR = PROJECT_ROOT / "evaluators" / "llm-judge"

# Schema definitions
REQUIRED_RUBRIC_FIELDS = ["code", "label", "weight", "aggregation_method", "passing_threshold", "benchmarks"]
REQUIRED_BENCHMARK_FIELDS = ["code", "parent_rubric", "label", "concept", "weight", "threshold", "criticality"]
VALID_EVALUATOR_TYPES = ["code", "llm_judge", "hybrid", "manual_sme"]
VALID_CRITICALITY = ["hard_gate", "threshold_gate"]
VALID_AGGREGATION = ["WEIGHTED_AVERAGE", "MINIMUM", "MAXIMUM", "MEAN"]


def load_yaml(path: Path) -> dict[str, Any] | None:
    """Load a YAML file, return None on error."""
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except Exception as e:
        return None


def validate_rubrics(rubrics: dict[str, dict], benchmarks: dict[str, dict]) -> list[str]:
    """Check rubric → benchmark references and schema."""
    errors = []
    
    for code, rubric in rubrics.items():
        # Required fields
        for field in REQUIRED_RUBRIC_FIELDS:
            if field not in rubric:
                errors.append(f"RUBRIC {code}: missing required field '{field}'")
        
        # Aggregation method enum
        agg = rubric.get("aggregation_method")
        if agg and agg not in VALID_AGGREGATION:
            errors.append(f"RUBRIC {code}: invalid aggregation_method '{agg}' (valid: {VALID_AGGREGATION})")
        
        # Benchmark references
        benchmark_refs = rubric.get("benchmarks", [])
        for ref in benchmark_refs:
            if ref not in benchmarks:
                errors.append(f"RUBRIC {code}: references benchmark '{ref}' which does not exist")
    
    return errors


def validate_benchmarks(benchmarks: dict[str, dict], rubrics: dict[str, dict], prompts: set[str]) -> list[str]:
    """Check benchmark → rubric and benchmark → prompt references and schema."""
    errors = []
    
    for code, benchmark in benchmarks.items():
        # Required fields
        for field in REQUIRED_BENCHMARK_FIELDS:
            if field not in benchmark:
                errors.append(f"BENCHMARK {code}: missing required field '{field}'")
        
        # Parent rubric reference
        parent = benchmark.get("parent_rubric")
        if parent and parent not in rubrics:
            errors.append(f"BENCHMARK {code}: parent_rubric '{parent}' does not exist")
        
        # Criticality enum
        crit = benchmark.get("criticality")
        if crit and crit not in VALID_CRITICALITY:
            errors.append(f"BENCHMARK {code}: invalid criticality '{crit}' (valid: {VALID_CRITICALITY})")
        
        # Evaluator type enum
        eval_type = benchmark.get("evaluator_type")
        if eval_type and eval_type not in VALID_EVALUATOR_TYPES:
            errors.append(f"BENCHMARK {code}: invalid evaluator_type '{eval_type}' (valid: {VALID_EVALUATOR_TYPES})")
        
        # Prompt file reference (required for llm_judge and hybrid)
        prompt_file = benchmark.get("llm_prompt_file")
        if eval_type in ["llm_judge", "hybrid"]:
            if not prompt_file:
                errors.append(f"BENCHMARK {code}: evaluator_type '{eval_type}' requires llm_prompt_file")
            elif prompt_file:
                # Normalize path
                prompt_name = Path(prompt_file).name
                if prompt_name not in prompts:
                    errors.append(f"BENCHMARK {code}: llm_prompt_file '{prompt_file}' does not exist")
        
        # Threshold range
        threshold = benchmark.get("threshold")
        if threshold is not None:
            if not (0.0 <= threshold <= 1.0):
                errors.append(f"BENCHMARK {code}: threshold {threshold} out of range [0.0, 1.0]")
    
    return errors


def find_orphan_prompts(benchmarks: dict[str, dict], prompts: set[str]) -> list[str]:
    """Find prompt files not referenced by any benchmark."""
    referenced = set()
    for benchmark in benchmarks.values():
        prompt_file = benchmark.get("llm_prompt_file")
        if prompt_file:
            referenced.add(Path(prompt_file).name)
    
    orphans = prompts - referenced - {"PROMPT_SPECS.md", "AGENTS.md"}  # Exclude spec and agent files
    return [f"ORPHAN: prompt '{p}' not referenced by any benchmark" for p in sorted(orphans)]


def check_bidirectional(rubrics: dict[str, dict], benchmarks: dict[str, dict]) -> list[str]:
    """Check that benchmark parent_rubric matches rubric benchmarks[] listing."""
    warnings = []
    
    for code, benchmark in benchmarks.items():
        parent = benchmark.get("parent_rubric")
        if parent and parent in rubrics:
            rubric_benchmarks = rubrics[parent].get("benchmarks", [])
            if code not in rubric_benchmarks:
                warnings.append(f"WARNING: benchmark '{code}' claims parent '{parent}' but is not listed in rubric's benchmarks[]")
    
    return warnings


def check_shared_prompts(benchmarks: dict[str, dict]) -> list[str]:
    """Flag benchmarks sharing the same prompt but with different thresholds/criticality.
    
    Per PROMPT_SPECS.md 'single behavior per judge' principle, benchmarks with different
    thresholds or criticality should have dedicated prompts to avoid conflated evaluation.
    """
    warnings = []
    
    # Group benchmarks by llm_prompt_file
    prompt_to_benchmarks: dict[str, list[tuple[str, dict]]] = {}
    for code, benchmark in benchmarks.items():
        prompt_file = benchmark.get("llm_prompt_file")
        if prompt_file:
            prompt_name = Path(prompt_file).name
            if prompt_name not in prompt_to_benchmarks:
                prompt_to_benchmarks[prompt_name] = []
            prompt_to_benchmarks[prompt_name].append((code, benchmark))
    
    # Check groups with multiple benchmarks
    for prompt_name, benchmark_list in prompt_to_benchmarks.items():
        if len(benchmark_list) < 2:
            continue
        
        # Extract thresholds and criticality
        thresholds = {code: b.get("threshold") for code, b in benchmark_list}
        criticalities = {code: b.get("criticality") for code, b in benchmark_list}
        
        unique_thresholds = set(thresholds.values())
        unique_criticalities = set(criticalities.values())
        
        # Flag if different thresholds or criticality
        if len(unique_thresholds) > 1 or len(unique_criticalities) > 1:
            codes = [code for code, _ in benchmark_list]
            details = ", ".join(f"{c}(t={thresholds[c]}, {criticalities[c]})" for c in codes)
            warnings.append(
                f"SHARED_PROMPT: '{prompt_name}' used by benchmarks with different thresholds/criticality: {details}. "
                f"Consider separate prompts per 'single behavior per judge' principle."
            )
    
    return warnings


def main():
    parser = argparse.ArgumentParser(description="Validate rubric/benchmark/prompt consistency")
    parser.add_argument("--report", type=str, help="Write report to file (markdown)")
    args = parser.parse_args()
    
    # Load all files
    rubrics = {}
    for f in RUBRICS_DIR.glob("*.yaml"):
        data = load_yaml(f)
        if data and "code" in data:
            rubrics[data["code"]] = data
    
    benchmarks = {}
    for f in BENCHMARKS_DIR.glob("*.yaml"):
        data = load_yaml(f)
        if data and "code" in data:
            benchmarks[data["code"]] = data
    
    prompts = {f.name for f in PROMPTS_DIR.glob("*.md")}
    
    # Run validations
    errors = []
    errors.extend(validate_rubrics(rubrics, benchmarks))
    errors.extend(validate_benchmarks(benchmarks, rubrics, prompts))
    errors.extend(find_orphan_prompts(benchmarks, prompts))
    errors.extend(check_bidirectional(rubrics, benchmarks))
    errors.extend(check_shared_prompts(benchmarks))
    
    # Summary
    summary = f"""# Consistency Validation Report

## Summary

- **Rubrics**: {len(rubrics)}
- **Benchmarks**: {len(benchmarks)}
- **Prompts**: {len(prompts) - 2} (excluding PROMPT_SPECS.md, AGENTS.md)
- **Issues Found**: {len(errors)}

## Issues

"""
    if errors:
        for e in sorted(errors):
            summary += f"- {e}\n"
    else:
        summary += "No issues found.\n"
    
    # Output
    if args.report:
        report_path = PROJECT_ROOT / args.report
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w") as f:
            f.write(summary)
        print(f"Report written to {report_path}")
    else:
        print(summary)
    
    # Exit code
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()

