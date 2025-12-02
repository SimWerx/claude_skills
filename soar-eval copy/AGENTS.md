# Agent Instructions — soar-pydantic-eval

## Purpose

Define evaluation **Rubrics** and **Benchmarks** for the SOAR framework. This is a medical SME research project for creating structured evaluation criteria — not an operational implementation.

## Quickstart

**Validate consistency** and get current inventory:

```bash
python3 tools/validate_consistency.py                    # Print summary + issues
python3 tools/validate_consistency.py --report reports/consistency.md  # Write report
```

Current workflow is manual YAML/markdown creation with validator checks.

## Architecture

```
soar-pydantic-eval/
├── AGENTS.md              # This file — project-wide guidance
├── CLAUDE.md              # Quick links for Claude Code
├── docs/                  # Supporting documentation
│   ├── rubric-benchmark-overview.md   # Conceptual hierarchy
│   ├── lag-boolean-prompt-spec.md     # LLM judge research
│   └── labeling_guide.md              # Human labeling guidance
├── rubrics/               # Rubric definitions
│   ├── AGENTS.md          # Rubric-specific instructions (READ FIRST)
│   └── FIELD_SPECS.md     # Rubric field specs
├── benchmarks/            # Benchmark definitions
│   ├── AGENTS.md          # Benchmark-specific instructions (READ FIRST)
│   ├── FIELD_SPECS.md     # Benchmark field specs
│   └── a-component/       # A-component benchmark YAMLs
└── evaluators/
    └── llm-judge/         # LLM-as-a-judge prompts
        ├── AGENTS.md      # Prompt-specific instructions (READ FIRST)
        └── PROMPT_SPECS.md  # Prompt structure specs
```

**Current inventory**: Run `python3 tools/validate_consistency.py` for counts.

**Precedence**: Nested AGENTS.md files override root when guidance conflicts. Always read the nearest AGENTS.md before editing files in that folder.

## Reference Documentation

| Topic | Location |
|-------|----------|
| Rubric fields | `rubrics/FIELD_SPECS.md` |
| Benchmark fields | `benchmarks/FIELD_SPECS.md` |
| LLM prompt structure | `evaluators/llm-judge/PROMPT_SPECS.md` |
| LLM judge research | `docs/lag-boolean-prompt-spec.md` |
| Hierarchy and scoring | `docs/rubric-benchmark-overview.md` |
| Parent SOAR framework | `zy_experimental/soar-framework/soar-overview.md` |

## Conventions

**File Naming**:
- Rubrics: `{code}.yaml` (e.g., `A-PRT.yaml`)
- Benchmarks: `{code}.yaml` (e.g., `A-PRT1.yaml`, `A-CMP6-airport.yaml`)
- Code format: `{Component}-{Category}` (e.g., A-FCT, S-ACC, O-USR, R-RWO)

## Do/Don't

**DO**:
- Read the nested AGENTS.md before editing files in any folder
- Define rubrics before benchmarks (hierarchy flows down)
- Specify evaluator type: `code`, `llm_judge`, `hybrid`, or `manual_sme`
- Include `llm_prompt_file` for `llm_judge` and `hybrid` types
- Run validator before committing

**DON'T**:
- Create benchmarks without a parent rubric
- Use vague scoring criteria without definition
- Skip threshold specification
- Assume tooling exists — document manual procedures first

## Domain Vocabulary

| Term | Definition |
|------|------------|
| Benchmark | Atomic measurable test within a rubric (e.g., A-NEG1) |
| Rubric | Organizational grouping of related benchmarks (e.g., A-NEG) |
| DII | DRAATT Intelligence Index — composite score across S/O/A/R pillars |
| Hard gate | Binary pass/fail that blocks deployment regardless of composite score |
| Threshold | Minimum acceptable score for a benchmark or rubric |

## PR & Commits

- `feat:` New rubric or benchmark
- `fix:` Correct threshold, weight, or definition error
- `docs:` Documentation updates
- `refactor:` Schema alignment or restructuring

## Safety & Permissions

- All content is synthetic — no real PHI
- SME review required before production use

### Allowed without asking
- Read/list any files
- Create/edit YAMLs in `rubrics/` and `benchmarks/a-component/`
- Create/edit prompts in `evaluators/llm-judge/`
- Update `WORKING.md` task tracking

### Require approval first
- Delete existing rubrics, benchmarks, or prompts
- Modify root `AGENTS.md` structure
- Restructure directory layout

## Related Resources

- **SOAR Framework**: `zy_experimental/soar-framework/soar-overview.md`
- **Metric Taxonomy**: `zy_experimental/soar-framework/soar-classification-codes-v0.1.json`
