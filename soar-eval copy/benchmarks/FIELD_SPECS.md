# Benchmark Field Specifications

This file defines the fields required when creating a **Benchmark**. For rubric-level fields, see `rubrics/FIELD_SPECS.md`.

Benchmark files live in `a-component/`. See `AGENTS.md` for the current inventory.

---

## Scope Boundary (applies to all A-component benchmarks)

A-component benchmarks test **Medic Copilot's behavior against known ground truth**, not clinical correctness.

| Benchmark Category | What It Tests | Where Clinical Knowledge Lives |
|--------------------|---------------|-------------------------------|
| **A-FCT, A-NEG, A-TMP, A-CMP, A-EVD, A-FMT** | Extraction/format accuracy — did AI extract stated information correctly? | Ground truth labels in test cases |
| **A-SFT, A-PRT, A-PED, A-CAR, A-STR, etc.** | System logic — does Medic Copilot's inference-time safety/protocol logic work? | Medic Copilot's knowledge base (Denver Metro protocols) |

**Key principle**: The eval harness provides test cases with **known ground truth**. It does NOT embed clinical formulas, dose ranges, or protocol rules. Those live in Medic Copilot's knowledge base. The eval harness checks whether Medic Copilot handles known test cases correctly.

**Example**:
- Correct: "Ground truth marks this dose as unsafe; did Medic Copilot flag it?"
- Wrong: "Is 324mg aspirin safe?" (clinical judgment belongs in Medic Copilot, not eval harness)

---

## What is a Benchmark?

A **Benchmark** is the actual measurable test or evaluation metric within a rubric.

**Example Benchmarks**:
```
Benchmark A-PRT1: DRAATT Section Coverage (25% of A-PRT)
  - Measures: Proportion of required DRAATT sections populated
  - Formula: (required_sections_populated / required_sections_with_content)
  - Threshold: >= 0.90
  - Evaluator: Code-based (section keyword detection)

Benchmark A-PRT2: Temporal Ordering Accuracy (25% of A-PRT)
  - Measures: Correctness of chronological event sequence
  - Formula: (correct_temporal_pairs / total_temporal_pairs)
  - Threshold: >= 0.85
  - Evaluator: Code-based (timestamp extraction and comparison)
```

---

## Benchmark Field Breakdown

When creating a Benchmark, provide the following information for each field:

### `code` (string, required)

**What it is**: Unique identifier for the benchmark
**Format**: Parent rubric code + number (e.g., "A-PRT1", "S-DOC2")
**Example**: `"A-PRT1"`

### `concept` (string, required)

**What it is**: Human-readable description of what is being measured
**Format**: Multi-sentence description covering: what, how, formula, threshold
**Example**: `"DRAATT Section Coverage - Proportion of required DRAATT sections populated when corresponding content exists in source narrative. Sections: Dispatch, Response, Arrival, Assessment, Treatment, Transport. Formula: (required_sections_populated / required_sections_with_content). Uses section keyword detection. Threshold: >=0.90."`

### `weight` (float, required)

**What it is**: Weight of this benchmark within its parent rubric
**Format**: 0.0 to 1.0 (e.g., 0.25 = 25%)
**Example**: `0.25` (25% of A-PRT rubric)

### `scoring_scale` (ScoringScale object, optional)

**What it is**: Defines the scale and normalization for this benchmark
**See**: ScoringScale Field Breakdown below

### `metric` (Metric object, optional)

**What it is**: The actual measurement/evaluator implementation
**Note**: This field is typically left for the implementation phase (populated by coding agent)

---

### `evaluator_type` (enum, required)

**What it is**: Type of evaluator used to compute this benchmark
**Options**: `code`, `llm_judge`, `hybrid`, `manual_sme`
**Example**: `evaluator_type: hybrid`

### `llm_prompt_file` (string, optional)

**What it is**: Path to LLM-as-a-judge prompt file (required for `llm_judge` and `hybrid` types)
**Format**: Relative path from repo root
**Example**: `llm_prompt_file: "evaluators/llm-judge/negation_simple_prompt.md"`

---

## ScoringScale Field Breakdown

Define the scoring scale for benchmarks:

### `min_value` (number, required)

**What it is**: Minimum possible score
**Example**: `0.0`

### `max_value` (number, required)

**What it is**: Maximum possible score
**Example**: `1.0`

### `descriptions` (dictionary, optional)

**What it is**: Descriptions for key score levels
**Format**: Dict mapping score values to descriptions
**Example**:
```yaml
descriptions:
  1.0: "Perfect accuracy"
  0.95: "Excellent (95%+)"
  0.90: "Very good (90-95%)"
  0.80: "Good (80-90%)"
  0.70: "Fair (70-80%)"
  0.60: "Poor (60-70%)"
  0.0: "Failed"
```

### `normalization_formula` (string, optional)

**What it is**: Formula to normalize raw scores to 0-1 range
**Format**: String formula (e.g., "x", "x/100", "(x-min)/(max-min)")
**Example**: `"x"` (already normalized to 0-1)

---

## Complete Example: A-NEG1 Benchmark

```yaml
# Benchmark: A-NEG1 — Simple Negation Handling
code: A-NEG1
parent_rubric: A-NEG
label: Simple Negation Misinterpretation

concept: >
  Straightforward denials or negated symptoms in the narrative (e.g., 'denies chest pain',
  'no shortness of breath') are encoded incorrectly in Medic Copilot's structured fields.

weight: 0.25
threshold: 0.90

scoring_scale:
  min_value: 0.0
  max_value: 1.0
  normalization_formula: "x"
  descriptions:
    1.0: "All simple negations correctly interpreted"
    0.90: "Excellent (90%+ correct)"
    0.80: "Good (80-90% correct)"
    0.70: "Fair (70-80% correct)"
    0.0: "Failed - negations systematically misinterpreted"

inclusion_criteria: >
  Apply when clear single-layer negation appears in ASR/narrative or ground truth and the
  output records the corresponding symptom or condition as present rather than absent.

exclusion_criteria: >
  Do not use for complex or double-negative phrasing (use A-NEG2/A-NEG3 instead).

examples:
  - "Narrative: 'patient denies chest pain' but output marks chest_pain: true."
  - "Ground truth includes 'fever' in negatives but output leaves fever unset."

evaluator_type: hybrid
llm_prompt_file: "evaluators/llm-judge/negation_simple_prompt.md"
```

---

## Evaluator Types

When defining benchmarks, use these standardized `evaluator_type` values:

| Value | Description | Use When |
|-------|-------------|----------|
| `code` | Automated script/validator | Deterministic metrics (F1, accuracy, coverage) |
| `llm_judge` | LLM evaluates with rubric prompt | Subjective quality, coherence, clinical judgment |
| `manual_sme` | Human expert review | Safety-critical, complex clinical reasoning |
| `hybrid` | Code + LLM | Complex metrics needing verification |

**LLM prompts**: See `evaluators/llm-judge/PROMPT_SPECS.md`. When using `llm_judge` or `hybrid`, include the `llm_prompt_file` field.

---

## Inclusion and Exclusion Criteria Format

These fields define WHEN a benchmark applies. They will be parsed by LLMs during code generation, so consistent structure is critical.

### `inclusion_criteria` (string, required)

**What it is**: Describes when this benchmark should be applied to a test case.

**Standard format** (two-part structure):
```
Apply when [TRIGGER]. Flag if [FAILURE CONDITION(S)].
```

**Rules**:
1. **First clause** starts with "Apply when" — describes when this benchmark is relevant
2. **Second clause** starts with "Flag if" — describes what constitutes a failure
3. Use "or" for alternative failure modes (implicit OR relationship)
4. Use "and" only when multiple conditions must co-occur
5. **Do NOT use numbered lists** like `(1)`, `(2)`, `(3)` — use natural connectors

**Good example**:
```yaml
inclusion_criteria: >
  Apply when multiple data points over time show the patient improving or worsening.
  Flag if the output misrepresents the trend direction, implies stability when vitals
  show decline, or fails to reflect improvement after intervention.
```

**Bad example** (numbered lists):
```yaml
inclusion_criteria: >
  Apply when: (1) condition A; (2) condition B; (3) condition C.
```

### `exclusion_criteria` (string, required)

**What it is**: Describes when this benchmark should NOT be applied, even if inclusion criteria are met.

**Important**: `exclusion_criteria` is for cases where the benchmark is NOT APPLICABLE (skip evaluation entirely). Cases that ARE applicable but should PASS (e.g., correctly handled edge cases, documented overrides) belong in the prompt's pass conditions or acceptable variations—not here.

**Standard format**:
```
Do not apply when [EXCEPTION]. Also exclude [ADDITIONAL EXCEPTION].
```

**Rules**:
1. Start with "Do not apply when" or "Do not use for"
2. List exceptions using natural connectors ("or", "and", commas)
3. Reference other benchmarks when delegating scope (e.g., "use A-NEG2 instead")
4. **Do NOT use numbered lists**

**Good example**:
```yaml
exclusion_criteria: >
  Do not apply for single pre/post comparisons (covered by A-TMP2) or when changes
  are minimal such that a trend is not clinically apparent.
```
