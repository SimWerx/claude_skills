# SOAR Rubric & Benchmark Information Request

> **ARCHIVED**: This document has been distilled into README.md and nested CLAUDE.md files. 
> Preserved here for provenance. See README.md for current project documentation.
> 
> **Original Last Updated**: 2025-01-24
> **Archived**: 2025-11-26

**Purpose**: This document guides the creation of evaluation Rubrics and Benchmarks for the SOAR (Synthetic data Orchestration, Assessment, and Refinement) implementation in the synthetic-data-epcr-narrative project.

**Intended Workflow**:
1. Fill out this template with evaluation criteria and reference standards
2. Completed template is handed to coding agent
3. Coding agent maps the information into project markdown files (templates, validators, documentation)

---

## How Rubrics and Benchmarks Interact

### Rubric (Evaluation Category)
A **Rubric** is an organizational grouping of related evaluation criteria that focuses on a specific quality dimension. It answers:
- **What area** are we evaluating? (e.g., Preservation Tracking, Safety Flag Tracking, Factual Correctness)
- **Why** does this category matter? (e.g., ensures semantic meaning preservation, detects safety issues)
- **How** do we aggregate scores from individual tests? (weighted average, minimum threshold, etc.)
- **What's** the passing threshold for this category?

**Example Rubric**:
```
Code: A-PRT
Label: Preservation Tracking (Automated)
Description: Measures preservation of semantic meaning and clinical intent through
             automated structural and temporal analysis.
Weight: 20% of A-Component
Passing Threshold: >= 0.80 (80%)
Aggregation: Weighted average of 4 benchmarks
```

### Benchmark (Specific Test/Metric)
A **Benchmark** is the actual measurable test or evaluation metric within a rubric. Each benchmark defines:
- **What exactly** is being measured? (e.g., "DRAATT Section Coverage", "Temporal Ordering Accuracy")
- **How** is it calculated? (formula, automated script, LLM-as-a-judge prompt)
- **What's** the passing threshold for this specific test?
- **How much** does this test contribute to the rubric score? (weight)

**Example Benchmarks for Above Rubric**:
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

Benchmark A-PRT3: Clinical Entity Preservation (25% of A-PRT)
  - Measures: Retention of clinical entities (symptoms, findings, meds)
  - Formula: (entities_in_output / entities_in_source)
  - Threshold: >= 0.80
  - Evaluator: Code-based (NER tagging)

Benchmark A-PRT4: Negation Handling Accuracy (25% of A-PRT)
  - Measures: Correct preservation of negative findings and scope
  - Formula: (correct_negations / total_negations)
  - Threshold: >= 0.90
  - Evaluator: Code-based (negation detection + dependency parsing)
```

### How They Work Together

**Hierarchy**:
```
Rubric: A-PRT (Preservation Tracking) - Weight: 20%, Threshold: 80%
├── Benchmark: A-PRT1 (Section Coverage) - Weight: 25%, Threshold: 90%
├── Benchmark: A-PRT2 (Temporal Ordering) - Weight: 25%, Threshold: 85%
├── Benchmark: A-PRT3 (Entity Preservation) - Weight: 25%, Threshold: 80%
└── Benchmark: A-PRT4 (Negation Handling) - Weight: 25%, Threshold: 90%
```

**Scoring Flow**:
1. Each **Benchmark** runs its evaluator (code-based or LLM-as-a-judge) and produces a score (0.0-1.0)
2. **Rubric** aggregates benchmark scores using weighted average
3. Final rubric score compared to rubric passing threshold

**Example Calculation**:
```
A-PRT1 score: 0.95 (95% section coverage) × 0.25 weight = 0.2375
A-PRT2 score: 0.88 (88% temporal ordering) × 0.25 weight = 0.2200
A-PRT3 score: 0.82 (82% entity preservation) × 0.25 weight = 0.2050
A-PRT4 score: 0.92 (92% negation handling) × 0.25 weight = 0.2300
───────────────────────────────────────────────────────────
A-PRT total: 0.8925 (89.25%) ✓ PASS (threshold: 80%)
```

**Analogy**:
- **Rubric** = Course (e.g., "English 101" with overall grade threshold)
- **Benchmark** = Individual assignments/tests (essay, midterm, final) each with its own weight and grade
- Final course grade = weighted average of all assignments

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
**Example**: `"Measures preservation of semantic meaning and clinical intent through automated structural and temporal analysis. Covers DRAATT section coverage, temporal ordering, entity preservation, and negation handling."`

### `passing_threshold` (float, required)
**What it is**: Minimum score required for the rubric to pass
**Format**: 0.0 to 1.0 (e.g., 0.80 = 80%)
**Default**: 0.80
**Example**: `0.80` (80%)

### `evaluation_guidelines` (object, optional)
**What it is**: Structured guidance for evaluators (see EvaluationGuidelines section below)
**Example**: See EvaluationGuidelines breakdown

### `benchmarks` (list of Benchmark objects, required for leaf rubrics)
**What it is**: The specific tests/metrics that make up this rubric
**Format**: List of Benchmark objects
**Example**: List of 4 benchmarks (A-PRT1 through A-PRT4)

### `sub_rubrics` (list of Rubric objects, optional)
**What it is**: Nested rubrics for hierarchical evaluation (use instead of benchmarks for composite rubrics)
**Format**: List of Rubric objects
**Example**: A-Component contains A-FCT, A-PRT, A-SFT sub-rubrics

---

## Benchmark Field Breakdown

When creating a Benchmark, provide the following information for each field:

### `code` (string, required)
**What it is**: Unique identifier for the benchmark
**Format**: Parent rubric code + number (e.g., "A-PRT1", "S-DOC2")
**Example**: `"A-PRT1"`

### `concept` (string, required)
**What it is**: Human-readable description of what is being measured, including formula and threshold
**Format**: Multi-sentence description covering: what, how, formula, threshold
**Example**: `"DRAATT Section Coverage - Proportion of required DRAATT sections populated when corresponding content exists in source narrative. Sections: Dispatch, Response, Arrival, Assessment, Treatment, Transport. Formula: (required_sections_populated / required_sections_with_content). Uses section keyword detection. Threshold: >=0.90."`

### `weight` (float, required)
**What it is**: Weight of this benchmark within its parent rubric
**Format**: 0.0 to 1.0 (e.g., 0.25 = 25%)
**Example**: `0.25` (25% of A-PRT rubric)

### `scoring_scale` (ScoringScale object, optional)
**What it is**: Defines the scale and normalization for this benchmark (see ScoringScale section below)
**Example**: See ScoringScale breakdown

### `metric` (Metric object, optional)
**What it is**: The actual measurement/evaluator implementation (populated by coding agent)
**Note**: This field is typically left for the implementation phase

---

## EvaluationGuidelines Field Breakdown

Provide structured guidance for evaluators:

### `focus_areas` (list of strings)
**What it is**: Key questions or areas evaluators should examine
**Format**: List of specific questions
**Example**:
```python
[
    "Section coverage: Are required DRAATT sections populated when content exists?",
    "Temporal ordering: Events in correct chronological sequence?",
    "Entity preservation: Clinical entities (symptoms, findings, interventions) retained?",
    "Negation handling: Negative findings and refusals correctly preserved?"
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
**Example**: `"Automated metrics must provide: (1) section coverage map with required vs present, (2) temporal graph showing event ordering, (3) entity tracking showing preservation rates, (4) negation analysis showing correct vs incorrect scope."`

### `special_instructions` (string, optional)
**What it is**: Additional context or special handling instructions
**Format**: Free-form guidance
**Example**: `"Focus on clinical impact of structural changes. DRAATT reorganization is acceptable if temporal causality preserved. Weight safety-critical negations (no allergies, refusal of care) more heavily."`

---

## ScoringScale Field Breakdown

Define the scoring scale for benchmarks:

### `name` (string, required)
**What it is**: Name identifying this scoring scale
**Example**: `"Automated Metrics 0-1"`

### `min_value` (number, required)
**What it is**: Minimum possible score
**Example**: `0.0`

### `max_value` (number, required)
**What it is**: Maximum possible score
**Example**: `1.0`

### `descriptions` (dictionary, optional)
**What it is**: Descriptions for key score levels (previously called `level_descriptions`)
**Format**: Dict mapping score values to descriptions
**Example**:
```python
{
    1.0: "Perfect accuracy",
    0.95: "Excellent (95%+)",
    0.90: "Very good (90-95%)",
    0.80: "Good (80-90%)",
    0.70: "Fair (70-80%)",
    0.60: "Poor (60-70%)",
    0.0: "Failed"
}
```

### `normalization_formula` (string, optional)
**What it is**: Formula to normalize raw scores to 0-1 range
**Format**: String formula (e.g., "x", "x/100", "(x-min)/(max-min)")
**Example**: `"x"` (already normalized to 0-1)

---

## Complete Example: A-PRT (Preservation Tracking) Rubric

Here's a real example from the SOAR implementation showing all fields populated:

```python
Rubric(
    code="A-PRT",
    label="Preservation Tracking (Automated)",
    description="Measures preservation of semantic meaning and clinical intent through automated structural and temporal analysis. Covers DRAATT section coverage, temporal ordering, entity preservation, and negation handling.",
    weight=0.20,  # 20% of A-Component
    aggregation_method=AggregationMethod.WEIGHTED_AVERAGE,
    passing_threshold=0.80,  # 80%
    evaluation_guidelines=EvaluationGuidelines(
        focus_areas=[
            "Section coverage: Are required DRAATT sections populated when content exists?",
            "Temporal ordering: Events in correct chronological sequence?",
            "Entity preservation: Clinical entities (symptoms, findings, interventions) retained?",
            "Negation handling: Negative findings and refusals correctly preserved?"
        ],
        acceptable_deviations=[
            "DRAATT reorganization if temporal logic maintained",
            "Combining related findings within same section",
            "Expanding abbreviations that preserve clinical meaning"
        ],
        critical_requirements=[
            "Required DRAATT sections must be identified from template specification",
            "Temporal markers must be extracted and sequenced",
            "Named entities must be tagged and tracked through pipeline",
            "Negation scope must be analyzed for clinical accuracy"
        ],
        evidence_requirements="Automated metrics must provide: (1) section coverage map with required vs present, (2) temporal graph showing event ordering, (3) entity tracking showing preservation rates, (4) negation analysis showing correct vs incorrect scope.",
        special_instructions="Focus on clinical impact of structural changes. DRAATT reorganization is acceptable if temporal causality preserved. Weight safety-critical negations (no allergies, refusal of care) more heavily."
    ),
    benchmarks=[
        # Benchmark 1: DRAATT Section Coverage
        Benchmark(
            code="A-PRT1",
            concept="DRAATT Section Coverage - Proportion of required DRAATT sections populated when corresponding content exists in source narrative. Sections: Dispatch, Response, Arrival, Assessment, Treatment, Transport. Formula: (required_sections_populated / required_sections_with_content). Uses section keyword detection. Threshold: >=0.90.",
            weight=0.25,  # 25% of A-PRT
            scoring_scale=ScoringScale(
                name="Automated Metrics 0-1",
                min_value=0.0,
                max_value=1.0,
                descriptions={
                    1.0: "Perfect accuracy",
                    0.95: "Excellent (95%+)",
                    0.90: "Very good (90-95%)",
                    0.80: "Good (80-90%)",
                    0.70: "Fair (70-80%)",
                    0.60: "Poor (60-70%)",
                    0.0: "Failed"
                },
                normalization_formula="x"  # Already 0-1 normalized
            )
        ),

        # Benchmark 2: Temporal Ordering Accuracy
        Benchmark(
            code="A-PRT2",
            concept="Temporal Ordering Accuracy - Correctness of chronological sequence: assessment before treatment, interventions in order, condition changes sequenced, cause-effect relationships preserved. Extract timestamps and relative temporal markers. Formula: (correct_temporal_pairs / total_temporal_pairs). Threshold: >=0.85.",
            weight=0.25,  # 25% of A-PRT
            scoring_scale=ScoringScale(
                name="Automated Metrics 0-1",
                min_value=0.0,
                max_value=1.0,
                descriptions={
                    1.0: "Perfect accuracy",
                    0.95: "Excellent (95%+)",
                    0.90: "Very good (90-95%)",
                    0.80: "Good (80-90%)",
                    0.70: "Fair (70-80%)",
                    0.60: "Poor (60-70%)",
                    0.0: "Failed"
                },
                normalization_formula="x"
            )
        ),

        # Benchmark 3: Clinical Entity Preservation
        Benchmark(
            code="A-PRT3",
            concept="Clinical Entity Preservation - Retention of clinical entities through processing: symptoms, physical findings, diagnoses, interventions, medications, devices. Use NER tagging. Formula: (entities_in_output / entities_in_source). Threshold: >=0.80.",
            weight=0.25,  # 25% of A-PRT
            scoring_scale=ScoringScale(
                name="Automated Metrics 0-1",
                min_value=0.0,
                max_value=1.0,
                descriptions={
                    1.0: "Perfect accuracy",
                    0.95: "Excellent (95%+)",
                    0.90: "Very good (90-95%)",
                    0.80: "Good (80-90%)",
                    0.70: "Fair (70-80%)",
                    0.60: "Poor (60-70%)",
                    0.0: "Failed"
                },
                normalization_formula="x"
            )
        ),

        # Benchmark 4: Negation Handling Accuracy
        Benchmark(
            code="A-PRT4",
            concept="Negation Handling Accuracy - Correct preservation of negative findings and scope: symptoms denied, treatments refused, findings absent, contraindications noted. Use negation detection with dependency parsing. Formula: (correct_negations / total_negations). Threshold: >=0.90 (strict - negation errors are clinically significant).",
            weight=0.25,  # 25% of A-PRT
            scoring_scale=ScoringScale(
                name="Automated Metrics 0-1",
                min_value=0.0,
                max_value=1.0,
                descriptions={
                    1.0: "Perfect accuracy",
                    0.95: "Excellent (95%+)",
                    0.90: "Very good (90-95%)",
                    0.80: "Good (80-90%)",
                    0.70: "Fair (70-80%)",
                    0.60: "Poor (60-70%)",
                    0.0: "Failed"
                },
                normalization_formula="x"
            )
        )
    ]
)
```

**Scoring Example**:
```
A-PRT1 score: 0.95 (95% section coverage) × 0.25 weight = 0.2375
A-PRT2 score: 0.88 (88% temporal ordering) × 0.25 weight = 0.2200
A-PRT3 score: 0.82 (82% entity preservation) × 0.25 weight = 0.2050
A-PRT4 score: 0.92 (92% negation handling) × 0.25 weight = 0.2300
───────────────────────────────────────────────────────────
A-PRT total: 0.8925 (89.25%) ✓ PASS (threshold: 80%)
```

---

## Submission Checklist

Before handing off completed information, verify:

- [ ] Each Rubric dimension has a clear evaluation scale
- [ ] Each Rubric dimension has scoring criteria for all levels
- [ ] Each Benchmark provides concrete examples at multiple quality levels
- [ ] Examples are drawn from or applicable to the synthetic-data-epcr-narrative project
- [ ] Related validators/tools are identified for each criterion
- [ ] Edge cases and common mistakes are documented

---

## Questions to Consider

1. **Scope**: Which aspects of the 4-pass workflow do Rubrics/Benchmarks cover?
   - Pass 1 (scaffold quality)?
   - Pass 2 (strategic planning quality)?
   - Pass 3 (narrative quality)?
   - Pass 4 (validation accuracy)?
   - All of the above?

2. **Granularity**: Should Rubrics be:
   - Template-specific (separate for full-draatt, doa, airport-transfer, rsi-overlay)?
   - Universal (apply to all templates)?
   - A mix (some universal, some template-specific)?

3. **Automation**: Which Rubric dimensions can be automated via validators vs require
   human/LLM judgment?

4. **Failure Modes**: What are the most critical failure modes to catch?
   - YAML-body inconsistency?
   - Implausible artifacts?
   - Template non-compliance?
   - Missing required content?

5. **Thresholds**: What minimum scores qualify as "acceptable" for production use?

---

## Next Steps

1. **Co-worker**: Fill out Rubric and Benchmark templates above
2. **Return**: Provide completed markdown to project lead
3. **Coding agent**: Map completed information into:
   - Template-specific AGENTS.md files
   - Validator enhancement specifications
   - Quality gate documentation in runbooks/
   - SOAR workflow integration points

---

**Contact**: [Add contact information for questions]

**Last Updated**: 2025-01-24

