# SOAR Pydantic Eval

Define evaluation **Rubrics** and **Benchmarks** for the SOAR framework to assess LLM application quality in medical documentation workflows.

## Purpose

This project guides medical SMEs in creating structured evaluation criteria for the SOAR (Synthetic data Orchestration, Assessment, and Refinement) framework. Completed rubrics and benchmarks will be handed to coding agents for implementation as validators, quality gates, and evaluation suites.

**Intended Workflow**:
1. SME defines rubrics and benchmarks using templates in this project
2. Completed definitions are reviewed for clinical accuracy
3. Coding agent maps definitions into validators and evaluation tooling
4. Evaluation suite integrates with the synthetic-data-gen validation pipeline

## Directory Structure

See `AGENTS.md` for the authoritative architecture map showing all rubrics, benchmarks, and prompt files.

```
soar-pydantic-eval/
├── AGENTS.md              # Agent instructions (start here)
├── CLAUDE.md              # Quick links for Claude Code
├── WORKING.md             # Active task tracking
├── rubrics/               # Rubric definitions (*.yaml)
│   └── FIELD_SPECS.md     # Rubric field specifications
├── benchmarks/            # Benchmark definitions
│   ├── FIELD_SPECS.md     # Benchmark field specifications
│   └── a-component/       # A-component benchmarks (*.yaml)
├── evaluators/
│   └── llm-judge/         # LLM-as-a-judge prompts
│       └── PROMPT_SPECS.md
└── docs/                  # Supporting documentation
```

## How Rubrics and Benchmarks Interact

### Rubric (Evaluation Category)

A **Rubric** is an organizational grouping of related evaluation criteria. It defines:
- What quality dimension is being evaluated
- How benchmark scores are aggregated (weighted average, minimum, etc.)
- The passing threshold for the category

### Benchmark (Specific Test)

A **Benchmark** is the actual measurable test within a rubric. It defines:
- What exactly is being measured
- The evaluator type (code, llm_judge, hybrid, manual_sme)
- The passing threshold and weight within its rubric

### Scoring Flow

1. Each **Benchmark** produces a score (0.0-1.0)
2. **Rubric** aggregates benchmark scores using its aggregation method
3. Final rubric score compared to rubric passing threshold

## Scope Boundary (Critical for Implementation)

A-component benchmarks test **Medic Copilot's behavior against known ground truth**, not clinical correctness.

| Category | What Eval Harness Tests | Where Clinical Knowledge Lives |
|----------|------------------------|-------------------------------|
| **Extraction** (A-FCT, A-NEG, A-TMP, A-CMP, A-EVD, A-FMT) | Did AI extract stated information correctly? | Ground truth labels in test cases |
| **System Logic** (A-SFT, A-PRT, A-PED, A-CAR, etc.) | Does Medic Copilot's inference-time logic work? | Medic Copilot's knowledge base (Denver protocols) |
| **Clinical Judgment** (S-component) | Is output clinically appropriate? | SME human review (not automated) |

**Key principle**: The eval harness provides test cases with **known ground truth**. It does NOT embed clinical formulas, dose ranges, or protocol rules. Those live in Medic Copilot's knowledge base.

**Example**:
- Correct: "Ground truth marks this dose as unsafe; did Medic Copilot flag it?"
- Wrong: "Is 324mg aspirin safe?" (clinical judgment belongs in Medic Copilot)

## Developer Handoff

### YAML → Pydantic Mapping

- Each `rubrics/*.yaml` → one `Rubric` Pydantic model
- Each `benchmarks/a-component/*.yaml` → one `Benchmark` Pydantic model
- Field specs in `*/FIELD_SPECS.md` define the schema

### Evaluator Implementation

| `evaluator_type` | Implementation |
|------------------|----------------|
| `code` | Python function (deterministic metrics) |
| `llm_judge` | Use prompt from `llm_prompt_file` field |
| `hybrid` | Code pre-check + LLM verification |
| `manual_sme` | Human expert review interface |

### Test Case Structure

Each test case must include ground truth labels:
- **Extraction benchmarks** (A-FCT, A-NEG): Ground truth provides expected extraction values
- **System logic benchmarks** (A-SFT, A-PRT, A-PED): Ground truth marks what Medic Copilot should detect/flag

### Provenance

This project evolved from `docs/archive/SOAR_rubric_handoff.md`. Key changes:
- Switched from Python inline to YAML definition files
- Added scope boundary clarifications (extraction vs system logic vs clinical judgment)
- Separated LLM prompts into reusable `.md` files
- Documented ground truth testing approach in `FIELD_SPECS.md` preambles

## Getting Started

**For Medical SMEs**:
1. Check `WORKING.md` for current tasks
2. Review existing rubrics in `rubrics/` and benchmarks in `benchmarks/a-component/`
3. Use field specs (`FIELD_SPECS.md`) when creating new definitions

**For Developers**:
1. Read `AGENTS.md` for project conventions and architecture
2. Review scope boundary in `benchmarks/FIELD_SPECS.md`
3. Map YAML definitions to Pydantic models
4. Implement evaluators per `evaluator_type` field

## Related Resources

- **SOAR Framework**: `zy_experimental/soar-framework/soar-overview.md`
- **Metric Taxonomy**: `zy_experimental/soar-framework/soar-classification-codes-v0.1.json`
- **Parent Project**: `synthetic-data-gen/` (ASR transcript generation and validation)

## Evaluation Flow

How Rubric YAMLs, Benchmark YAMLs, and LLM prompts connect:

```
                    ┌─────────────────────────────────────┐
                    │  Rubric YAML (A-FCT.yaml)           │
                    │  - Aggregation logic                │
                    │  - Weight: 0.125 of A-component     │
                    │  - Threshold: 0.85                  │
                    └─────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
            │ Benchmark    │ │ Benchmark    │ │ Benchmark    │
            │ A-FCT1.yaml  │ │ A-FCT2.yaml  │ │ A-FCT3.yaml  │
            │ weight: 0.40 │ │ weight: 0.25 │ │ weight: 0.15 │
            └──────────────┘ └──────────────┘ └──────────────┘
                    │               │               │
                    ▼               ▼               ▼
            ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
            │ LLM Prompt   │ │ LLM Prompt   │ │ LLM Prompt   │
            │ vitals_...md │ │ meds_...md   │ │ proc_...md   │
            │              │ │              │ │              │
            │ RUBRIC:      │ │ RUBRIC:      │ │ RUBRIC:      │
            │ (how to      │ │ (how to      │ │ (how to      │
            │  judge)      │ │  judge)      │ │  judge)      │
            └──────────────┘ └──────────────┘ └──────────────┘
                    │               │               │
                    ▼               ▼               ▼
              pass/fail       pass/fail       pass/fail
                    │               │               │
                    └───────────────┼───────────────┘
                                    ▼
                    ┌─────────────────────────────────────┐
                    │  Rubric YAML aggregates scores      │
                    │  A-FCT = 0.40×FCT1 + 0.25×FCT2 + ...│
                    └─────────────────────────────────────┘
```