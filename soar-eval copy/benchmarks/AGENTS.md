# Agent Instructions — benchmarks/

## Read First

**Before creating or editing any benchmark YAML:**

1. Read `FIELD_SPECS.md` in this directory — it defines all required fields, formats, and validation rules.
2. Reference existing benchmarks in `a-component/` as templates for structure and style.

## Critical Patterns: Criteria Format

### inclusion_criteria

```
Apply when [TRIGGER CONDITION]. Flag if [FAILURE CONDITION(S)].
```

- First clause: "Apply when" — describes when benchmark is relevant
- Second clause: "Flag if" — describes what constitutes failure

### exclusion_criteria

```
Do not apply when [EXCEPTION]. Also exclude [ADDITIONAL EXCEPTION].
```

- Start with "Do not apply when" or "Do not use for"
- Use natural connectors ("or", "and", commas) — NOT numbered lists

## Validation Tools

Run after editing benchmarks to ensure compliance:

```bash
python3 tools/validate_benchmark_criteria.py  # Check criteria format
python3 tools/validate_consistency.py         # Check relationships
```

## File Locations

- `FIELD_SPECS.md` — Authoritative field definitions
- `a-component/*.yaml` — A-component benchmark definitions (46 files)

## Allowed Without Asking

- Read/list any files
- Create/edit benchmark YAMLs following FIELD_SPECS.md patterns
- Add examples to existing benchmarks

## Require Approval First

- Delete existing benchmarks
- Modify FIELD_SPECS.md schema
- Change benchmark codes or parent rubric assignments
- Rebalance weights across a rubric

