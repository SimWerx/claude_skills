# Agent Instructions — rubrics/

## Read First

**Before creating or editing any rubric YAML:**

1. Read `FIELD_SPECS.md` in this directory — it defines all required fields, aggregation methods, and evaluation guidelines structure.
2. Reference existing rubrics in this directory as templates for structure and style.

## Critical Pattern: Rubric-Benchmark Hierarchy

- Rubrics group related benchmarks (e.g., A-FCT contains A-FCT1, A-FCT2, A-FCT3, A-FCT4)
- Benchmarks must exist before being added to a rubric's `benchmarks` list
- Benchmark weights within a rubric should sum to ~1.0

## Rubric Code Format

```
{Component}-{Category}
```

- A-component: A-NEG, A-FCT, A-TMP, A-EVD, A-CMP, A-SFT, A-PRT, A-FMT, A-PED, A-CAR, A-REF, A-STR, A-TRM, A-OBS, A-BHV, A-UNC
- S-component: S-ACC, S-SFT, S-DOC (future)
- O-component: O-USR (future)
- R-component: R-RWO (future)

## File Locations

- `FIELD_SPECS.md` — Authoritative field definitions
- `*.yaml` — Rubric definitions (16 files)

## Allowed Without Asking

- Read/list any files
- Create/edit rubric YAMLs following FIELD_SPECS.md patterns
- Update evaluation_guidelines content
- Add benchmarks to rubric's benchmarks list (if benchmark exists)

## Require Approval First

- Delete existing rubrics
- Modify FIELD_SPECS.md schema
- Change rubric codes
- Modify aggregation_method or passing_threshold
- Create new rubric categories

