# Rubric Field Specifications

This file defines the fields required when creating a **Rubric**. For benchmark fields, see `benchmarks/FIELD_SPECS.md`.

Rubric files live in this directory. See `AGENTS.md` for the current inventory.

For the full research basis on LLM-as-a-judge evaluation design, see `docs/lag-boolean-prompt-spec.md`.

---

## Scope Boundary (applies to all A-component rubrics)

A-component rubrics (A-NEG, A-FCT, A-SFT, A-PRT, etc.) group benchmarks that test **Medic Copilot's behavior against known ground truth**.

| Rubric Type | What Benchmarks Test | Where Clinical Knowledge Lives |
|-------------|---------------------|-------------------------------|
| **Extraction rubrics** (A-FCT, A-NEG, A-TMP, A-CMP, A-EVD, A-FMT) | Did AI extract stated information correctly? | Ground truth labels in test cases |
| **System logic rubrics** (A-SFT, A-PRT, A-PED, A-CAR, A-STR, etc.) | Does Medic Copilot's inference-time logic work? | Medic Copilot's knowledge base (Denver Metro protocols) |

**Key principle**: Rubrics define evaluation categories and aggregation methods. Clinical rules (dose ranges, protocols, contraindications) live in Medic Copilot's knowledge base, not the eval harness. The eval harness checks whether Medic Copilot handles known test cases correctly.

**Note**: S-component rubrics (S-ACC, S-SFT, S-DOC) involve SME clinical judgment and are not covered by automated A-component evaluation.

---

## What is a Rubric?

A **Rubric** is an organizational grouping of related evaluation criteria that focuses on a specific quality dimension.

**Example Rubric**:
```
Code: A-PRT
Label: Preservation Tracking (Automated)
Description: Measures preservation of semantic meaning and clinical intent
             through automated structural and temporal analysis.
Weight: 20% of A-Component
Passing Threshold: >= 0.80 (80%)
Aggregation: Weighted average of 4 benchmarks
```

---

## Rubric Field Breakdown

When creating a Rubric, provide the following information for each field:

### `code` (string, required)

**What it is**: Unique identifier for the rubric
**Format**: Short code (e.g., "A-PRT", "S-DOC", "DII")
**Example**: `"A-PRT"`

### `label` (string, required)

**What it is**: Human-readable name for the rubric
**Format**: Descriptive title
**Example**: `"Preservation Tracking (Automated)"`

### `weight` (float, required)

**What it is**: Weight of this rubric within its parent rubric (or component)
**Format**: 0.0 to 1.0 (e.g., 0.20 = 20%)
**Default**: 1.0
**Example**: `0.20` (20% of A-Component)

### `aggregation_method` (enum, required)

**What it is**: How to combine benchmark scores into the rubric score
**Options**:
- `WEIGHTED_AVERAGE`: Multiply each benchmark score by its weight and sum
- `MINIMUM`: Use the lowest benchmark score
- `MAXIMUM`: Use the highest benchmark score
**Example**: `AggregationMethod.WEIGHTED_AVERAGE`

### `description` (string, optional)

**What it is**: Detailed explanation of what the rubric evaluates and why it matters
**Format**: 1-3 sentences
**Example**: `"Measures preservation of semantic meaning and clinical intent through automated structural and temporal analysis."`

### `passing_threshold` (float, required)

**What it is**: Minimum score required for the rubric to pass
**Format**: 0.0 to 1.0 (e.g., 0.80 = 80%)
**Default**: 0.80
**Example**: `0.80` (80%)

### `evaluation_guidelines` (EvaluationGuidelines object, optional)

**What it is**: Structured guidance for evaluators
**See**: EvaluationGuidelines Field Breakdown below

### `benchmarks` (list of Benchmark objects, required for leaf rubrics)

**What it is**: The specific tests/metrics that make up this rubric
**Format**: List of Benchmark objects
**Example**: List of 4 benchmarks (A-PRT1 through A-PRT4)

### `sub_rubrics` (list of Rubric objects, optional)

**What it is**: Nested rubrics for hierarchical evaluation (use instead of benchmarks for composite rubrics)
**Format**: List of Rubric objects
**Example**: A-Component contains A-FCT, A-PRT, A-SFT sub-rubrics

---

## EvaluationGuidelines Field Breakdown

Provide structured guidance for evaluators within a rubric:

### `focus_areas` (list of strings)

**What it is**: Key questions or areas evaluators should examine
**Format**: List of specific questions
**Example**:
```python
[
    "Section coverage: Are required DRAATT sections populated when content exists?",
    "Temporal ordering: Events in correct chronological sequence?",
    "Entity preservation: Clinical entities retained?",
    "Negation handling: Negative findings correctly preserved?"
]
```

### `acceptable_deviations` (list of strings)

**What it is**: Variations that are acceptable and should not be penalized
**Format**: List of specific acceptable changes
**Example**:
```python
[
    "DRAATT reorganization if temporal logic maintained",
    "Combining related findings within same section",
    "Expanding abbreviations that preserve clinical meaning"
]
```

### `critical_requirements` (list of strings)

**What it is**: Non-negotiable requirements that must be met
**Format**: List of must-have criteria
**Example**:
```python
[
    "Required DRAATT sections must be identified from template specification",
    "Temporal markers must be extracted and sequenced",
    "Named entities must be tagged and tracked through pipeline",
    "Negation scope must be analyzed for clinical accuracy"
]
```

### `evidence_requirements` (string, optional)

**What it is**: What evidence must be provided to support the evaluation
**Format**: Description of required artifacts/documentation
**Example**: `"Automated metrics must provide: (1) section coverage map, (2) temporal graph, (3) entity tracking rates, (4) negation analysis."`

### `special_instructions` (string, optional)

**What it is**: Additional context or special handling instructions
**Format**: Free-form guidance
**Example**: `"Focus on clinical impact of structural changes. Weight safety-critical negations more heavily."`

---

## Complete Example: A-REF Rubric (YAML Format)

This example shows the actual YAML format used in rubric files:

```yaml
# Rubric: A-REF — Refusal Documentation
# Evaluates completeness of patient refusal documentation

code: A-REF
label: Refusal Documentation
description: >
  Evaluates documentation of patient refusal scenarios including explanation
  of risks and benefits, patient capacity assessment, and refusal signature
  or witness documentation. Critical because refusals are the highest
  medicolegal risk area in EMS.

weight: 0.125
aggregation_method: WEIGHTED_AVERAGE
passing_threshold: 0.95

evaluation_guidelines:
  focus_areas:
    - "Were risks of refusal explained and documented?"
    - "Is the patient's reason for refusal captured?"
    - "Is refusal signature or witness documentation present?"
    - "Was patient capacity assessment documented?"
  acceptable_deviations:
    - "Minor wording differences in risk explanation if content is preserved"
    - "Paraphrased patient reasoning that preserves intent"
  critical_requirements:
    - "Risk explanation MUST be documented if stated in narrative"
    - "Patient acknowledgment of risks MUST be captured"
    - "Signature or witness info MUST appear if documented in narrative"
  evidence_requirements: >
    Refusal documentation check: (1) risks explained and acknowledged,
    (2) patient reasoning, (3) signature/witness status.

benchmarks:
  - A-REF1  # Risks not explained/documented
  - A-REF2  # Signature/witness missing
```

**Scoring Example** (WEIGHTED_AVERAGE aggregation):
```
A-REF1: 1.00 × 0.60 = 0.60  (threshold 1.0, hard_gate)
A-REF2: 0.90 × 0.40 = 0.36  (threshold 0.85, threshold_gate)
─────────────────────────────
A-REF total: 0.96 PASS (threshold: 95%)
```

---

## Score Aggregation from Benchmarks

Rubric scores are computed from individual benchmark results:

### Benchmark to Rubric Flow

1. **LLM Judge** returns `{"pass": bool, "reason": str, "score": float}` per test case
2. **Benchmark score** = mean of `score` values across all test cases for that benchmark
3. **Rubric score** = aggregation of benchmark scores using `aggregation_method`

### Default Score Mapping

Per the research spec (`docs/lag-boolean-prompt-spec.md`):
- `pass = true` → `score = 1.0`
- `pass = false` → `score = 0.0`

### Hard Gates vs. Threshold Gates

| Criticality | Behavior |
|-------------|----------|
| `hard_gate` | If benchmark fails (score < threshold), entire rubric fails regardless of other scores |
| `threshold_gate` | Benchmark score contributes to weighted average; rubric can still pass if aggregate meets threshold |

---

## Related Documentation

- **Research basis**: `docs/lag-boolean-prompt-spec.md` — LLM-as-a-judge design principles
- **Benchmark field specs**: `benchmarks/FIELD_SPECS.md` — Individual benchmark definitions
- **LLM prompt specs**: `evaluators/llm-judge/PROMPT_SPECS.md` — Prompt structure for judges
- **Rubric-benchmark overview**: `docs/rubric-benchmark-overview.md` — Conceptual hierarchy
